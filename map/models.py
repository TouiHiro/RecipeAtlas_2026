from django.db import models

# Create your models here.
class Map(models.Model):
  region_id = models.AutoField(primary_key=True)
  region_name = models.CharField(max_length=30)
