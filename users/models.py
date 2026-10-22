from django.db import models
from django.conf import settings
from map.models import Map
# Create your models here.

class User(models.Model):
    # autofieldにはprimary_key以外は入れない
    user_id = models.AutoField(max_length=100, verbose_name="ユーザーid", primary_key=True)
    user_name = models.CharField(max_length=100, verbose_name="ユーザー名")
    user_personality = models.CharField(null=True, max_length=100, verbose_name="ユーザーパーソナリティ")
    user_detail = models.CharField(null=True, max_length=100, verbose_name="ユーザー詳細")
    user_icon = models.ImageField(null=True, blank=True, upload_to="user_icons/", verbose_name="ユーザーアイコン")
    region_id = models.ForeignKey(Map, on_delete=models.CASCADE, verbose_name="土地ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")

# relationクラス

class Relation(models.Model):
    relation_id = models.AutoField(primary_key=True,on_delete=models.CASCADE, related_name='フォローID', )
    followee_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='フォロイ―ID' )
    follower_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='フォロワ―ID' )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    