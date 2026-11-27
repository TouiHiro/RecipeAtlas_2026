from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from .models import *


class MapResource(resources.ModelResource):
    class Meta:
        model = Map
        import_id_fields = ("region_id",)  # 'id' ではなく 'region_id' を識別子にする
        fields = ("region_id", "region_name")


@admin.register(Map)
class MapAdmin(ImportExportActionModelAdmin):
    resource_classes = [MapResource]
    list_display = ("region_id", "region_name")
    search_fields = ["region_name", "region_id"]