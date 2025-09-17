from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Category
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .forms import CategoryForm
from django.db.models import Count

class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            product_count=Count('products')
        ).order_by('-product_count')

        search_item = self.request.GET.get('search_name')
        if search_item:
            queryset = queryset.filter(name__icontains=search_item)
        

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_categories'] = Category.objects.count()
        context['total_products_in_categories'] = Category.objects.aggregate(
            total=Count('products')
        )['total'] or 0
        context['total_active_categories'] = Category.objects.filter(
        products__batches__quantity__gt=0).distinct().count() or 0

        return context

class CreateCategory(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/modal_form.html"
    success_url = reverse_lazy('categories:category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Добавление категории'
        context['action'] = 'Добавить категорию'
        context['theme'] = 'green'  # или 'red', 'blue'
        return context

class DeleteCategory(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'products/modal_delete.html'
    success_url = reverse_lazy('categories:category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['item'] = 'категорию'
        context['info'] = f'категорию: {category}'

        return context

class EditCategory(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'products/modal_form.html'
    success_url = reverse_lazy('categories:category-list')