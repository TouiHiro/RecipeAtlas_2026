from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import *
# Register your models here.


@admin.register(Ingredients)
class IngredientAdmin(ImportExportActionModelAdmin):
    list_display = ("index_number", "name", "energy", "carbs", "fat", "protein", "sugar", "sodium")
    search_fields = ["name", "index_number"]
    
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("recipe_title", "created_at")
    search_fields = ["recipe_title"]

#次回動くか確認
# @admin.resister(RecipeIngredient)
# class RecipeIngredientAdmin(admin.ModelAdmin):
#     list_display = ("recipe", "Ingredient", "weight")
#     search_fields = ("recipe")

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Process)
