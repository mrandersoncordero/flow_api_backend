from django.contrib import admin

# Models
from .models import Commission

@admin.register(Commission)
class ComissionAdmin(admin.ModelAdmin):
    list_display = ["id", "description", "status", "petition", "active", "created"]
    list_display_links = ["id"]
    list_editable = ["active", "status"]
    list_filter = ["status", "created", "active"]
    search_fields = ["description", "status"]

    fieldsets = (
        (
            None,
            {
                "fields": ("description", ("status", "petition", "active")),
            },
        ),
        ("Metadata", {"fields": (("created", "modified", "deleted"))}),
    )
    readonly_fields = ("created", "modified", "deleted")
