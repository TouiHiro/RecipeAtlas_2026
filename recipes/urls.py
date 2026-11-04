from django.urls import path  # url から path に変更
from . import views

app_name = "recipes"

urlpatterns = [
    # path('', views.recipe_list, name='index'),
    path('form/', views.recipe_form, name='form'),
    path("page/<int:id>/", views.recipe_detail, name="recipe_detail"),
    path("page/<int:id>", views.recipe_update, name="recipe_update")
]