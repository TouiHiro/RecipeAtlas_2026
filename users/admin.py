from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(Relation)
admin.site.register(Favorite)
admin.site.register(Review)
# Register your models here.
