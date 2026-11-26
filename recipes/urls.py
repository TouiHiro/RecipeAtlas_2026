from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    
    # 共通部分の呼出し
    path("insert", views.recipe_form, name='recipe_insert'),
    path("search_ingredients/",views.search_ingredients,name="search_ingredients")
]
