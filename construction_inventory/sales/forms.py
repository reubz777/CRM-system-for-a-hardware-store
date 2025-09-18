from django import forms
from .models import Sale
from datetime import datetime
from warehouse.models import Batch

class SaleCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только активные партии и настраиваем подписи
        self.fields['batch'].queryset = Batch.objects.filter(quantity__gt=0).select_related(
            'product', 'product__category', 'product__supplier'
        ).order_by('product__name', '-arrival_date')
        self.fields['batch'].label_from_instance = (
            lambda b: f"{b.product.name} — {b.quantity} шт., {b.price} BYN, #{b.id}"
        )
    class Meta:
        model = Sale
        fields = "__all__"
        widgets = {
            'batch': forms.Select(attrs={
                'class': 'form-control select2-field',
                'data-placeholder': 'Начните вводить название товара...'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'sale_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'value': datetime.now().strftime('%Y-%m-%dT%H:%M')
            })
        }
        labels = {
            'batch': 'Выберите партию товара',
            'quantity': 'Количество',
            'sale_date': 'Дата и время продажи'
        }
        help_texts = {
            'quantity': 'Введите количество товара для продажи',
            'sale_date': 'Выберите дату и время совершения продажи'
        }