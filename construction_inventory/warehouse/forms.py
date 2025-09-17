from django import forms
from warehouse.models import Batch
from products.models import Product

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = '__all__'
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control product-select',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'arrival_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_products = Product.objects.select_related('category', 'supplier').all().order_by('name')

class BatchUpdate(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['price', 'quantity']
        widgets = {
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }