from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from molinks import views

app_name = 'molinks'

urlpatterns = [
    path('', include('links.urls')),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('admin/', admin.site.urls),
]
