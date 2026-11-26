from datetime import datetime
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from import_export import fields, resources, widgets
from import_export.admin import ImportExportActionModelAdmin
from map.models import Map
from .models import *


class FlexibleDateTimeWidget(widgets.DateTimeWidget):
    def clean(self, value, row=None, **kwargs):
        if not value:
            return timezone.now()
        s = str(value).strip().strip("'\"").replace("/", "-")
        for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
        ):
            try:
                dt = datetime.strptime(s, fmt)
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt)
                return dt
            except ValueError:
                continue
        return super().clean(s, row=row, **kwargs)


class UserResource(resources.ModelResource):
    created_at = fields.Field(
        column_name="created_at",
        attribute="created_at",
        widget=FlexibleDateTimeWidget(),
    )
    region = fields.Field(
        column_name="region_id",
        attribute="region",
        widget=widgets.ForeignKeyWidget(Map, field="pk"),
        default=None,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "user_personality",
            "user_detail",
            "user_icon",
            "region",
            "created_at",
        )


@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin, BaseUserAdmin):
    resource_classes = [UserResource]
    list_display = ("username", "email", "region", "user_personality", "created_at", "is_staff")
    search_fields = ["username", "email", "user_personality"]
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "プロフィール情報",
            {
                "fields": (
                    "user_personality",
                    "user_detail",
                    "user_icon",
                    "region",
                    "created_at",
                )
            },
        ),
    )