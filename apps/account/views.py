"""
Account views.
"""

# Django imports
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Models
from petitions.models import Petition


class DashBoardView(ListView, LoginRequiredMixin):
    template_name = "index.html"
    model = Petition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Petition.objects.all()
        context["petitions"] = queryset
        context["total_petitions"] = queryset.count()
        return context



