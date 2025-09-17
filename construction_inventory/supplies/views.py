from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Supplier
from products.models import Product
from warehouse.models import Batch
from .forms import SuppliesForm

class SuppliesList(LoginRequiredMixin,ListView):
    model = Supplier
    template_name = "supplies/suppliers.html"
    context_object_name = 'supplies'

    def get_queryset(self):
        queryset = super().get_queryset()

        search_param = self.request.GET.get('search')
        if search_param:
            queryset = Supplier.objects.filter(name__icontains=search_param)
            return queryset

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        supplier = Supplier.objects.all()
        context['total_supplies'] = supplier.count()
        context['total_products'] = Product.objects.count()
        context['total_batch'] = Batch.objects.filter(quantity__gt=0).count()
        return context


class SuppliesAdd(LoginRequiredMixin, CreateView):
    model = Supplier
    form_class = SuppliesForm
    template_name = 'products/modal_form.html'
    success_url = reverse_lazy('supplies:supplies-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить поставщика'
        context['action'] = 'Добавить поставщика'
        return context


class SuppliesEdit(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SuppliesForm
    template_name = 'products/modal_form.html'
    success_url = reverse_lazy('supplies:supplies-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать поставщика'
        context['action'] = 'Обновить'
        context['theme'] = 'green'
        return context


class SuppliesDelete(LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'products/modal_delete.html'
    success_url = reverse_lazy('supplies:supplies-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplies = self.get_object()
        context['item'] = 'поставщика'
        context['info'] = f'поставщика: {supplies}/{supplies.contact_face}/{supplies.telephone}/{supplies.email}'

        return context

