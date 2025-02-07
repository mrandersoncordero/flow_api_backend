# Django
from django.contrib import admin

# Models
from .models import Department, Petition

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id']
    list_editable = ['name']

    fieldsets = (
        (None, {
            "fields": (
                'name', 'active'
            ),
        }),
        ('Metadata', {
            'fields': (
                ('created', 'modified'),
            )
        })
    )
    
    readonly_fields = ('created', 'modified')
    

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'parent_petition', 'get_priority_display', 'get_status_approval_display']
    list_filter = ['priority', 'status_approval']
    search_fields = ['title', 'description']
    autocomplete_fields = ['parent_petition']

    def get_priority_display(self, obj):
        return obj.get_priority_display()  # Devuelve el valor legible del ChoiceField
    get_priority_display.short_description = "Priority"  # Nombre de la columna en Django Admin

    def get_status_approval_display(self, obj):
        return obj.get_status_approval_display()
    get_status_approval_display.short_description = "Status Approval"
