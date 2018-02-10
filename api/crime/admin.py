from django.contrib import admin

from .models import GVAIncident


class GVAIncidentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("date", "city_county", "gva_id", "injured", "killed", "state", "street",)
        }),
        ("Meta", {
            "classes": ("grp-collapse",),
            "fields": ("created", "id", "updated",)
        })
    )
    list_display = ("id", "date", "injured", "killed", "city_county", "state",)
    list_filter = ("state",)
    readonly_fields = ("created", "id", "updated",)
    search_fields = ()


admin.site.register(GVAIncident, GVAIncidentAdmin)
