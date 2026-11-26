from django.contrib import admin
from import_export import fields, resources, widgets
from import_export.admin import ImportExportActionModelAdmin
from map.models import Map
from users.models import User
from .models import Ingredients, Process, Recipe, RecipeIngredient, Tag


class RecipeResource(resources.ModelResource):
    user = fields.Field(
        column_name="user_id",
        attribute="user",
        widget=widgets.ForeignKeyWidget(User, field="pk"),
    )
    region = fields.Field(
        column_name="region_id",
        attribute="region",
        widget=widgets.ForeignKeyWidget(Map, field="pk"),
    )

    class Meta:
        model = Recipe
        import_id_fields = ("recipe_id",)
        fields = (
            "recipe_id",
            "user",
            "recipe_title",
            "recipe_img",
            "recipe_detail",
            "region",
            "created_at",
            "tag",
        )


class RecipeIngredientResource(resources.ModelResource):
    recipe = fields.Field(
        column_name="recipe_id",
        attribute="recipe",
        widget=widgets.ForeignKeyWidget(Recipe, field="recipe_id"),
    )
    Ingredient = fields.Field(
        column_name="Ingredient_id",
        attribute="Ingredient",
        widget=widgets.ForeignKeyWidget(Ingredients, field="pk"),
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "recipe", "Ingredient", "weight")


class ProcessResource(resources.ModelResource):
    recipe = fields.Field(
        column_name="recipe_id",
        attribute="recipe",
        widget=widgets.ForeignKeyWidget(Recipe, field="recipe_id"),
    )

    class Meta:
        model = Process
        import_id_fields = ("process_id",)
        fields = (
            "process_id",
            "process_num",
            "process_detail",
            "process_img",
            "recipe",
        )


@admin.register(Ingredients)
class IngredientAdmin(ImportExportActionModelAdmin):
    list_display = (
        "index_number",
        "name",
        "energy",
        "carbs",
        "fat",
        "protein",
        "sugar",
        "sodium",
    )
    search_fields = ["name", "index_number"]


@admin.register(Recipe)
class RecipeAdmin(ImportExportActionModelAdmin):
    resource_classes = [RecipeResource]
    list_display = ("recipe_id", "recipe_title", "user", "region", "created_at")
    search_fields = ["recipe_title", "user__username"]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(ImportExportActionModelAdmin):
    resource_classes = [RecipeIngredientResource]
    list_display = ("id", "recipe", "Ingredient", "weight")
    search_fields = ["recipe__recipe_title", "Ingredient__name"]


@admin.register(Process)
class ProcessAdmin(ImportExportActionModelAdmin):
    resource_classes = [ProcessResource]
    list_display = ("process_id", "recipe", "process_num", "process_detail")
    search_fields = ["process_detail", "recipe__recipe_title"]


@admin.register(Tag)
class TagAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name")
    search_fields = ["name"]