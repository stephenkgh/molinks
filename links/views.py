from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Category, Link
from . import forms

@login_required
def index(request):
    # process form
    errors = None
    if request.method == 'POST':
        form = forms.LinksForm(request.user, request.POST)
        if form.is_valid():
            cat = get_cat(request)
            if cat is None:
                errors = "Choose an existing category or create a new one"
            else:
                new_link = Link(url=request.POST['url'], note=request.POST['note'], category=cat, user=request.user)
                new_link.save()
                # reset form
                form = forms.LinksForm(request.user)
    else:
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
        'errors': errors,
        'link_heir': link_heir,
    })


@login_required
def edit_link(request, link_id):
    link = Link.objects.get(id=link_id)

    # process form
    errors = None
    if request.method == 'POST':
        # links are never deleted via the UI, just marked inactive
        if 'delete' in request.POST:
            link.active = False
            link.save()
        elif 'save' in request.POST:
            form = forms.LinksForm(request.user, request.POST)
            if form.is_valid():
                cat = get_cat(request)
                if cat is None:
                    errors = "Choose an existing category or create a new one"
                else:
                    (link.url, link.note, link.category) = (request.POST['url'], request.POST['note'], cat)
                    link.save()
        # go back to index page
        if errors is None:
            return HttpResponseRedirect(reverse('index'))

    else:
        form = forms.LinksForm(request.user, initial={
            'url': link.url,
            'note': link.note,
            'category': link.category,
        })

    # render template
    return render(request, 'links/edit_link.html', {
        'link_id': link.id,
        'form': form,
        'errors': errors,
    })


@login_required
def edit_cat(request, cat_id):
    cat = Category.objects.get(id=cat_id)

    # process form
    errors = None
    if request.method == 'POST':
        if 'delete' in request.POST:
            raise Exception("NotYetImplemented")
        elif 'save' in request.POST:
            form = forms.EditCatForm(request.POST)
            if form.is_valid():
                cat.name = request.POST['name']
                cat.save()
        # go back to index page
        if errors is None:
            return HttpResponseRedirect(reverse('index'))

    else:
        form = forms.EditCatForm(initial={
            'name': cat.name,
        })

    # render template
    return render(request, 'links/edit_cat.html', {
        'category': cat,
        'cat_id': cat.id,
        'form': form,
        'errors': errors,
    })


# ---- utility ---------------------------------------------------------------------------------------


def get_cat(request):
    # create new category
    cat = None
    if len(request.POST['new_cat']) > 0:
        cat = Category(name=request.POST['new_cat'], user=request.user)
        cat.save()
    # use existing category
    elif request.POST['category']:
        cat = Category.objects.get(id=request.POST['category'])

    return cat
