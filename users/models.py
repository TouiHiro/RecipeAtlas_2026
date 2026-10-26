from django.conf import settings

# Create your models here.

from django.db import models
# AbstractUserが便利
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from map.models import Map

class User(AbstractUser):
    user_personality = models.CharField(null=True, blank=True, max_length=100, verbose_name="ユーザーパーソナリティ")
    user_detail = models.CharField(null=True, blank=True, max_length=100, verbose_name="ユーザー詳細")
    user_icon = models.ImageField(null=True, blank=True, upload_to="user_icons/", verbose_name="ユーザーアイコン")
    region = models.ForeignKey(Map, on_delete=models.CASCADE, null=True, blank=True, verbose_name="土地ID")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="登録日時")

    def __str__(self):
        return self.username

# relationクラス

class Relation(models.Model):
    relation_id = models.AutoField(primary_key=True)
    followee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followee_user", verbose_name="フォローされている人")
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follower_user", verbose_name="フォローしている人")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    # ユニーク制約
    class Meta:
        unique_together = ('followee_id', 'follower_id')
    # 誰が誰をフォローしているかわかりやすいように
    def __str__(self):
        return f"{self.follower_id} -> {self.followee_id}"

# Favorite class
class Favorite(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_id" ,verbose_name="好いている人") 
    recipe = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipe_id" ,verbose_name="好かれてるレシピ") 

    def __str__(self):
        return f"{self.favorite_id}"