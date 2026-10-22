from django.db import models
from map.models import Map
from users.models import User

# Create your models here.

class Recipe(models.Model):
  recipe_id = models.AutoField(primary_key=True)
  user_id = models.ForeignKey(User ,on_delete=models.CASCADE)
  recipe_title = models.CharField(30)
  recipe_detail = models.CharField(100)
  region_id = models.ForeignKey(User ,on_delete=models.CASCADE)
  created_at = models.dateField(auto_now_add=True)
  tag = models.CharField(10)

