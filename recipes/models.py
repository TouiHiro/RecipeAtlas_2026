from django.db import models
from django.conf import settings  # 追加
from map.models import Map
from users.models import User

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipe_user")
    recipe_title = models.CharField(max_length=30)
    recipe_detail = models.CharField(max_length=300)
    region = models.ForeignKey(Map, on_delete=models.CASCADE, related_name="recipe_region")
    created_at = models.DateField(auto_now_add=True)
    tag = models.CharField(max_length=10)

    def __str__(self):
        return self.recipe_title

class Process(models.Model):
    process_id = models.AutoField(primary_key=True)
    process_num = models.IntegerField(max_length=2)
    process_detail = models.CharField(max_length=300)
    recipe_id = models.ForeignKey(Recipe,on_delete=models.CASCADE, related_name="process_recipe")

    def __str__(self):
        return f"{self.process_id}"