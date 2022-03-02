from django.urls import path

from . import views

app_name = 'links'

urlpatterns = [
    path('', views.index, name='index'),
    path('link/<int:link_id>', views.edit_link, name='edit_link'),
    path('category/<int:cat_id>', views.edit_cat, name='edit_cat'),
]
