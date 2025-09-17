from django.contrib import admin
from .models import Product
from warehouse.models import Batch, BatchGroup
from categories.models import Category

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    # Поля которые отображаются в списке
    list_display = [
        'id',
        'product',
        'group',
        'price',
        'quantity',
        'arrival_date',
        'is_modified'
    ]

    # Поля по которым можно фильтровать
    list_filter = [
        'product',
        'group',
        'arrival_date',
        'is_modified'
    ]

    # Поля по которым можно искать
    search_fields = [
        'product__name',
        'group__id'
    ]

    # Поля которые отображаются в форме редактирования
    fields = [
        'product',
        'group',
        'price',
        'quantity',
        'arrival_date',
        'is_modified'
    ]

    # Поля только для чтения
    readonly_fields = [
        'arrival_date',
        'is_modified'
    ]


@admin.register(BatchGroup)
class BatchGroupAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'created_date',
        'total_quantity'  # кастомное property
    ]

    list_filter = [
        'product',
        'created_date'
    ]

    search_fields = [
        'product__name'
    ]

    readonly_fields = [
        'created_date',
        'total_quantity'
    ]


# Остальные модели можно оставить как есть
admin.site.register(Product)
admin.site.register(Category)