from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
import calendar
from django.db.models import Sum, Count, Avg, F
from django.utils import timezone
from datetime import datetime
from .forms import ProductForm
from .models import Product
from django.db.models.functions import TruncMonth
from warehouse.models import Batch
from sales.models import Sale

class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        queryset = queryset.prefetch_related('batches')
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['total_product'] = Product.objects.count()
        context['total_in_stock'] = len((list(product for product in context['object_list'] if product.total_quantity > 0)))
        context['total_out_stock'] =  context['total_product']-context['total_in_stock']
        return context

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_card.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return Product.objects.prefetch_related('batches')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_batches = context['product'].batches.all()[:1][0]
        context['price'] = last_batches.price
        context['arrival_date'] = last_batches.arrival_date
        batches = context['product'].batches.all()
        context['batches'] = batches

        # Подсчёт активных партий
        active_batches = [batch for batch in batches if batch.quantity > 0]
        context['active_batches'] = active_batches
        context['active_batches_count'] = len(active_batches)

        # Первичные состояния историй по всем партиям товара
        initial_histories = []
        for batch in batches:
            initial = batch.history.order_by('history_date').first()
            if initial:
                initial_histories.append(initial)
        context['initial_histories'] = initial_histories
        context['initial_histories_count'] = len(initial_histories)
        return context

class CreateProduct(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/modal_form.html"
    success_url = reverse_lazy('products:product-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление товара'
        context['action'] = 'Добавить продукт'
        context['theme'] = 'green'  # green,red,blue

        return context

class UpdateProduct(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/modal_form.html'
    success_url = reverse_lazy('products:product-list')


class AnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'products/analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_year = timezone.now().year
        current_month = timezone.now().month

        years = list(range(current_year - 4, current_year + 1))
        years.reverse()

        months = {
            1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
            5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
            9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
        }

        selected_year = int(self.request.GET.get('year', current_year))
        selected_month = int(self.request.GET.get('month', current_month))


        monthly_stats = Sale.objects.annotate(
            month=TruncMonth('sale_date')
        ).values('month').annotate(
            monthly_revenue=Sum(F('quantity') * F('batch__price'))
        ).aggregate(
            total_revenue=Sum('monthly_revenue'),
            month_count=Count('month', distinct=True)
        )

        total_revenue = monthly_stats['total_revenue'] or 0
        month_count = monthly_stats['month_count'] or 0

        days_in_month = calendar.monthrange(selected_year,selected_month)[1]
        total_month_revenue = Sale.total_month_revenue(selected_year, selected_month)
        avg_profit = round((total_month_revenue/days_in_month),2)

        # Вычисляем среднюю выручку за предыдущие месяцы
        avg_previous_revenue = total_revenue / month_count if month_count > 0 else 0
        
        # Вычисляем процент роста относительно средней выручки
        if avg_previous_revenue > 0:
            profit_percentage = ((total_month_revenue - avg_previous_revenue) / avg_previous_revenue) * 100
        else:
            profit_percentage = 0 if total_month_revenue == 0 else 100

        chart_data = self.generate_chart_data(selected_year, selected_month)
        stats_data = self.calculate_stats(selected_year, selected_month)

        context.update({
            'years': years,
            'months': months,
            'selected_year': selected_year,
            'selected_month': selected_month,
            'current_year': current_year,
            'current_month': current_month,
            'chart_labels': chart_data['labels'],
            'chart_values': chart_data['values'],
            'chart_colors': chart_data['colors'],
            'avg_daily_revenue': chart_data['avg_daily_revenue'],
            'stats': stats_data,
            'profit_percentage': round(profit_percentage, 1),
            'avg_profit': avg_profit,
        })

        return context

    def generate_chart_data(self, year, month):
        
        # Получаем количество дней в месяце
        days_in_month = calendar.monthrange(year, month)[1]
        
        # Создаем массивы для данных
        labels = []
        values = []
        colors = []
        
        # Названия дней недели на русском
        weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        
        # Получаем среднюю выручку за день
        days_in_month = calendar.monthrange(year, month)[1]
        total_month_revenue = Sale.total_month_revenue(year, month)
        avg_daily_revenue = total_month_revenue / days_in_month if days_in_month > 0 else 0
        
        # Получаем реальные данные выручки по дням
        for day in range(1, days_in_month + 1):
            # Получаем выручку за день
            daily_revenue = Sale.objects.filter(
                sale_date__year=year,
                sale_date__month=month,
                sale_date__day=day
            ).aggregate(
                revenue=Sum(F('quantity') * F('batch__price'))
            )['revenue'] or 0
            
            # Получаем день недели
            date_obj = datetime(year, month, day)
            weekday_name = weekdays[date_obj.weekday()]
            
            # Определяем цвет на основе сравнения с средней выручкой
            if daily_revenue > avg_daily_revenue:
                color = 'rgba(40, 167, 69, 0.8)'  # Зеленый - выше среднего
            elif daily_revenue < avg_daily_revenue:
                color = 'rgba(220, 53, 69, 0.8)'  # Красный - ниже среднего
            else:
                color = 'rgba(108, 117, 125, 0.8)'  # Серый - равно среднему
            
            labels.append(f"{day}\n{weekday_name}")
            values.append(float(daily_revenue))
            colors.append(color)

        return {
            'labels': labels,
            'values': values,
            'colors': colors,
            'avg_daily_revenue': avg_daily_revenue
        }
    def calculate_stats(self, year, month):
        
        total_products = Product.objects.count()

        products_in_stock = Product.objects.filter(
            batches__quantity__gt=0
        ).distinct().count()

        products_out_of_stock = total_products - products_in_stock
        
        total_quantity = Batch.objects.aggregate(
            total=Sum('quantity')
        )['total'] or 0
        
        total_value = sum(
            batch.quantity * batch.price for batch in Batch.objects.all()
        )
        
        average_price = total_value / total_quantity if total_quantity > 0 else 0
        
        sales_in_period = Sale.objects.filter(
            sale_date__year=year,
            sale_date__month=month
        )
        
        total_sales = sales_in_period.count()
        total_revenue = sales_in_period.aggregate(
            revenue=Sum(F('quantity') * F('batch__price'))
        )['revenue'] or 0

        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        
        prev_sales = Sale.objects.filter(
            sale_date__year=prev_year,
            sale_date__month=prev_month
        ).count()

        growth_percentage = 0
        if prev_sales > 0:
            growth_percentage = ((total_sales - prev_sales) / prev_sales) * 100
        
        return {
            'total_products': total_products,
            'products_in_stock': products_in_stock,
            'products_out_of_stock': products_out_of_stock,
            'total_quantity': total_quantity,
            'total_value': total_value,
            'average_price': average_price,
            'total_sales': total_sales,
            'total_revenue': round(total_revenue, 2),
            'growth_percentage': round(growth_percentage, 1),
        }

class Manual(LoginRequiredMixin, TemplateView):
    template_name = 'products/manual_info.html'