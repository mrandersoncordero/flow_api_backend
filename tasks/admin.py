"""Task admin."""

# Django
from django.contrib import admin

# Models
from .models import Department, TaskStatus, Task


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ['name']
    ordering = ['-created']


@admin.register(TaskStatus)
class TaskStatuAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_editable = ['name']
    ordering = ['pk']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user__first_name',
                    'department', 'status', 'hours', 'created']
    search_fields = ['username', 'user__first_name',
                     'user__last_name', 'title', 'status']
    ordering = ['status', '-created']
    list_filter = ['title', 'department', 'status', 'created']

    raw_id_fields = ['user']

    fieldsets = (
        (None, {
            "fields": (
                ('title'),
                ('description'),
                ('user', 'department'),
                ('status', 'hours')
            ),
        }),
        ('Metadata', {
            "fields": (
                ('created', 'modified')
            )
        }),
    )

    readonly_fields = ('created', 'modified')
