from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from molinks import views

app_name = 'molinks'

urlpatterns = [
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html')),
    path('login/', views.login, name='login'),
    path('links/', include('links.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
