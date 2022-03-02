from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from django.utils import timezone

from .models import Category, Link
from . import forms

@login_required
def index(request):
    errors = False
    if request.method == 'POST':
        form = forms.LinksForm(request.user, request.POST)
        if form.is_valid():
            cat = None

            # create new category
            if len(request.POST['new_cat']) > 0:
                cat = Category(name=request.POST['new_cat'], user=request.user)
                cat.save()
            # use existing category
            elif request.POST['category']:
                cat = Category.objects.get(id=request.POST['category'])
            else:
                errors = "Choose an existing category or create a new one"

            if cat is not None:
                new_link = Link(url=request.POST['url'], note=request.POST['note'], category=cat, user=request.user)
                new_link.save()
                # reset form
                form = forms.LinksForm(request.user)

    else:
        form = forms.LinksForm(request.user)

    # process links and categories into heirarchy for display
    links = Link.objects.all(request.user)
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

    return render(request, 'links/index.html', {
        'form': form,
        'errors': errors,
        'link_heir': link_heir,
    })
