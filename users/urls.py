# users/urls.py

from django.urls import path
from . import views

urlpatterns = [

    path('login.html',views.login_page, name='login_page'),
    path('logon.html', views.logon_page, name='logon_page'),
    path('login_success_test.html', views.login_success_test_page, name='test_page_success')
]