from django.db import models
from django.conf import settings  # 追加
from map.models import Map
from users.models import User

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipe_user")
    recipe_title = models.CharField(max_length=30)
    recipe_detail = models.CharField(max_length=300)
    region = models.ForeignKey(Map, on_delete=models.CASCADE, related_name="recipe_region")
    created_at = models.DateField(auto_now_add=True)
    tag = models.CharField(max_length=10)

    def __str__(self):
        return self.recipe_title

class Ingredients(models.Model):
    category = models.CharField(max_length=10, verbose_name="食品群")
    index_number = models.CharField(max_length=10, verbose_name="索引番号")
    name = models.CharField(max_length=100, verbose_name="食品名", blank=True, null=True)
    energy = models.FloatField(verbose_name="エネルギー(kcal)", default=0)
    protein = models.FloatField(verbose_name="タンパク質(g)", default=0)
    fat = models.FloatField(verbose_name="脂質(g)", default=0)
    sugar = models.FloatField(verbose_name="糖質(g)", default=0)
    carbs = models.FloatField(verbose_name="炭水化物(g)", default=0)
    sodium = models.FloatField(verbose_name="塩分(g)", default=0)
    
    def __str__(self):
        return f"{self.index_number}:{self.name}"
    
class RecipeIngredient(models.Model):
    recipe= models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients")
    Ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, related_name="used_recipes")
    weight = models.FloatField(verbose_name="使用料(g)", default=0)
    
    def __str__(self):
        return f"{self.recipe.recipe_title} - {self.Ingredient.name}({self.weight})"
class Process(models.Model):
    process_id = models.AutoField(primary_key=True)
    process_num = models.IntegerField()
    process_detail = models.CharField(max_length=300)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE, related_name="process_recipe")

    def __str__(self):
        # Process番号だけだとわかりにくいから recipe_titleも欲しい 別クラスから引っ張ってくる方法わからん
        return f" {self.process_num} "
