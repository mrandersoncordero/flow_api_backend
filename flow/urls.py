"""URL configuration for flow project."""

# Django
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    path('', include('tasks.urls', namespace='tasks'))
]
