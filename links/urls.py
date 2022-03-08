from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recent/', views.recent, name='recent'),
    path('link/<int:link_id>', views.edit_link, name='edit_link'),
    path('category/<int:cat_id>', views.edit_cat, name='edit_cat'),
    path('theme/', views.choose_theme, name='choose_theme'),
]
