from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(Relation)
admin.site.register(Favorite)

# Register your models here.
