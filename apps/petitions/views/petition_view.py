# apps/petitions/views/petition_view.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.db.models import Count, Q
from django.utils.functional import cached_property

from petitions.models import Petition

class PetitionListView(LoginRequiredMixin, ListView):
    template_name = "petitions/list.html"
    context_object_name = "petitions"
    paginate_by = 20 # paginación

    # Helpers para filtros
    @cached_property
    def q(self):
        return self.request.GET.get("q", "").strip()

    @cached_property
    def priority(self):
        return self.request.GET.get("priority")

    @cached_property
    def status_approval(self):
        return self.request.GET.get("status")

    @cached_property
    def company_id(self):
        cid = self.request.GET.get("company")
        return int(cid) if cid and cid.isdigit() else None

    @cached_property
    def department_id(self):
        did = self.request.GET.get("department")
        return int(did) if did and did.isdigit() else None
    
    def get_queryset(self):
        qs = Petition.active_objects.select_related("company", "department", "user")

        if self.q:
            qs = qs.filter(
                Q(title__icontains=self.q) | Q(description__icontains=self.q)
            )
        
        if self.priority:
            qs = qs.filter(priority=self.priority)
        
        if self.status_approval:
            qs = qs.filter(status_approval=self.status_approval)
        
        if self.company_id:
            qs = qs.filter(company_id=self.company_id)

        if self.department_id:
            qs = qs.filter(department_id=self.department_id)

        return qs
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        base_qs = Petition.active_objects.all()

        ctx['counts_by_status'] = base_qs.values('status_approval').annotate(count=Count('id'))
        ctx['counts_by_priority'] = base_qs.values('priority').annotate(count=Count('id'))

        # Filtros activos
        ctx['filters'] = {
            'q': self.q,
            'priority': self.priority,
            'status_approval': self.status_approval,
            'company_id': self.company_id,
            'department_id': self.department_id,
        }

        return ctx