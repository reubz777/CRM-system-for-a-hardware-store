from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from .models import Sale
from django.db.models import F, Q
from .forms import SaleCreateForm
from django.urls import reverse_lazy

class SaleList(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sales.html'
    context_object_name = 'sales'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('batch__product')
        queryset = queryset.annotate(total_price = F('quantity')*F('batch__price'))

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        search_name  = self.request.GET.get('search')

        filters = Q()
        if start_date:
            filters &= Q(sale_date__gte=start_date)
        if end_date:
            filters &= Q(sale_date__lte=end_date)
        if search_name:
            filters &= Q(batch__product__name__icontains=search_name)
        if filters:
            queryset = queryset.filter(filters)

        queryset = queryset.order_by('-sale_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_revenue'] = Sale.total_revenue()
        context['sales_count'] = Sale.objects.count()
        context['avg_revenue'] = Sale.avg_revenue()
        return context


class SaleCreate(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleCreateForm
    template_name = "sales/modal_sale_create.html"
    success_url = reverse_lazy('sales:sales-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Всё, что нужно для кастомного селектора, есть в form.batch.queryset
        context['all_products'] = self.get_form().fields['batch'].queryset
        return context

