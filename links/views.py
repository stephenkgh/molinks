from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import NON_FIELD_ERRORS

from .models import Category, Link
from . import forms

@login_required
def index(request):
    # process form
    form = None
    if request.method == 'POST':
        form = forms.LinksForm(request.user, request.POST)
        if form.is_valid():
            cat = _get_cat(request)
            new_link = Link(url=request.POST['url'], note=request.POST['note'], category=cat, user=request.user)
            new_link.save()
            form = None # reset form
        else:
            # special case: if the only error is no category, autofocus on the new category field
            if len(form.errors[NON_FIELD_ERRORS]) == 1 and form.has_error(NON_FIELD_ERRORS, 'no_cat'):
                form.fields['url'].widget.attrs = {}
                form.fields['new_cat'].widget.attrs = {'autofocus': True}

    # build clean form
    if not form:
        form = forms.LinksForm(request.user)

    # process links and categories into heirarchy for display
    links = Link.objects.all(request.user).filter(active=True)
    link_heir = {}
    cat_id = None
    for link in links:
        if cat_id == link.category.id:
            link_heir[cat_id]['links'].append(link)
        else:
            cat_id = link.category.id
            link_heir[cat_id] = {
                'cat': link.category,
                'links': [link],
            }

    # render template
    return render(request, 'links/index.html', {
        'form': form,
        'link_heir': link_heir,
        'admin': request.user.is_staff,
    })


@login_required
def recent(request):
    # process form
    form = None
    if request.method == 'POST':
        form = forms.LinksForm(request.user, request.POST)
        if form.is_valid():
            cat = _get_cat(request)
            new_link = Link(url=request.POST['url'], note=request.POST['note'], category=cat, user=request.user)
            new_link.save()
            form = None # reset form
        else:
            # special case: if the only error is no category, autofocus on the new category field
            if len(form.errors[NON_FIELD_ERRORS]) == 1 and form.has_error(NON_FIELD_ERRORS, 'no_cat'):
                form.fields['url'].widget.attrs = {}
                form.fields['new_cat'].widget.attrs = {'autofocus': True}

    # build clean form
    if not form:
        form = forms.LinksForm(request.user)

    # process links and categories into heirarchy for display
    link_heir = Link.objects.all(request.user).filter(active=True).order_by('-updated')

    # render template
    return render(request, 'links/recent.html', {
        'form': form,
        'link_heir': link_heir,
        'admin': request.user.is_staff,
    })


@login_required
def edit_link(request, link_id):
    link = Link.objects.get(id=link_id)

    # process form
    form = None
    done = False
    if request.method == 'POST':
        # links are never deleted via the UI, just marked inactive
        if 'delete' in request.POST:
            link.active = False
            link.save()
            done = True
        elif 'save' in request.POST:
            form = forms.LinksForm(request.user, request.POST)
            if form.is_valid():
                cat = _get_cat(request)
                (link.url, link.note, link.category) = (request.POST['url'], request.POST['note'], cat)
                link.save()
                done = True
        else: # cancel
            done = True

    # go back to index page
    if done:
        return HttpResponseRedirect(reverse('index'))

    # build edit form
    if not form:
        form = forms.LinksForm(request.user, initial={
            'url': link.url,
            'note': link.note,
            'category': link.category,
        })

    # render template
    return render(request, 'links/edit_link.html', {
        'link_id': link.id,
        'form': form,
    })


@login_required
def edit_cat(request, cat_id):
    cat = Category.objects.get(id=cat_id)

    # process form
    form = None
    done = False
    if request.method == 'POST':
        form = forms.EditCatForm(request.POST)
        if 'delete' in request.POST:
            raise Exception("NotYetImplemented")
        elif 'save' in request.POST:
            if form.is_valid():
                cat.name = request.POST['name']
                cat.save()
                done = True
        else: # cancel
            done = True

    # go back to index page
    if done:
        return HttpResponseRedirect(reverse('index'))

    # build edit form
    if not form:
        form = forms.EditCatForm(initial={
            'name': cat.name,
        })

    # render template
    return render(request, 'links/edit_cat.html', {
        'category': cat,
        'cat_id': cat.id,
        'form': form,
    })


# ---- utility ---------------------------------------------------------------------------------------

def _get_cat(request):
    # create new category
    cat = None
    if len(request.POST['new_cat']) > 0:
        cat = Category(name=request.POST['new_cat'], user=request.user)
        cat.save()
    # use existing category
    elif request.POST['category']:
        cat = Category.objects.get(id=request.POST['category'])

    return cat
