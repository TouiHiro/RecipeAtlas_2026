# users/urls.py

from django.urls import path
from . import views

urlpatterns = [

    path('login.html',views.login_page, name='login_page'),
    path('test_home.html', views.test_home, name="test_home"),
    path('register.html', views.register_page, name='register_page'),
]