# Django
from django.contrib import admin

# Models
from .models import Department, Petition, Company


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "active"]
    list_display_links = ["id"]
    list_editable = ["name"]

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "active"),
            },
        ),
        ("Metadata", {"fields": (("created", "modified"),)}),
    )

    readonly_fields = ("created", "modified")

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "active"]
    list_display_links = ["id"]
    list_editable = ["name"]

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "active"),
            },
        ),
        ("Metadata", {"fields": (("created", "modified"),)}),
    )

    readonly_fields = ("created", "modified")

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "priority",
        "is_main",
        "active",
        "status_approval",
        "department",
    ]
    list_filter = ["priority", "status_approval", "created"]
    search_fields = ["title", "description"]

    # def get_priority_display(self, obj):
    #     return obj.get_priority_display()  # Devuelve el valor legible del ChoiceField

    # get_priority_display.short_description = (
    #     "Priority"  # Nombre de la columna en Django Admin
    # )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    ("status_approval", "priority"),
                    ("active", "department", "company"),
                    ("user", "is_main"),
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": (("created", "modified"),),
            },
        ),
    )

    readonly_fields = ["created", "modified"]
