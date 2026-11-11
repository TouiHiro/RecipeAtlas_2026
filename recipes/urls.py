from django.urls import path
from . import views

urlpatterns = [
    # 共通部分の呼出し
    path("", views.my_view, name='after_screen_base.html')
]