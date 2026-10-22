from django.db import models
from map.models import Map
# Create your models here.

class Users(models.Model):
    user_id = models.CharField(max_length=100, verbose_name="ユーザーid", primary_key=True)
    user_name = models.CharField(max_length=100, verbose_name="ユーザー名")
    user_personality = models.CharField(null=True, max_length=100, verbose_name="ユーザーパーソナリティ")
    user_detail = models.CharField(null=True, max_length=100, verbose_name="ユーザー詳細")
    user_icon = models.ImageField(null=True, blank=True, upload_to="user_icons/", verbose_name="ユーザーアイコン")
    region_id = models.ForeignKey(Map, on_delete=models.CASCADE, verbose_name="土地ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")

# relationクラス
class Relation(models.Model):
    