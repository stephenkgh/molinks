from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from molinks import views, loginviews

app_name = 'molinks'

urlpatterns = [
    # application
    path('', views.index, name='index'),
    path('recent/', views.recent, name='recent'),
    path('link/<int:link_id>', views.edit_link, name='edit_link'),
    path('category/<int:cat_id>', views.edit_cat, name='edit_cat'),
    path('theme/', views.choose_theme, name='theme'),

    # login management
    path('login/', loginviews.login, name='login'),
    path('logout/', loginviews.logout, name='logout'),

    # admin
    path('admin/', admin.site.urls),
]
