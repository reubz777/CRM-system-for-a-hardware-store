from django.core.exceptions import ValidationError
from django.db import models
from warehouse.models import Batch
from django.db.models import Sum, F, Avg

class Sale(models.Model):

    batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        related_name='sales',
        verbose_name="Партия товара"
    )
    quantity = models.PositiveIntegerField(default=1)
    sale_date = models.DateTimeField()

    class Meta:
        db_table = "Продажи"
        verbose_name = "Продажа"
        permissions = [
            ('can_view_sales', 'Может просматривать продажи'),
            ('can_make_sales', 'Может проводить продажи'),
            ('can_delete_sales', 'Может удалять продажи'),
            ('can_edit_sales', 'Может редактировать продажи'),
        ]

    def formatted_date(self):
        return self.sale_date.strftime("%d.%m.%Y %H:%M")

    def clean(self):
        if self.quantity > self.batch.quantity:
            raise ValidationError(
                f"Недостаточно товара. В наличии: {self.batch.quantity}"
            )

    def save(self, *args, **kwargs):
        self.full_clean()

        if self._state.adding:
            self.batch.quantity -= self.quantity
            self.batch.save()

        super().save(*args, **kwargs)

    @classmethod
    def total_revenue(cls):
        queryset = cls.objects.aggregate(
            total_revenue=Sum(F('quantity') * F('batch__price'))
        )
        return queryset.get('total_revenue', 0) or 0

    @classmethod
    def avg_revenue(cls):
        queryset = cls.objects.aggregate(
            avg_revenue= Avg(F('quantity') * F('batch__price'))
        )
        return queryset.get('avg_revenue',0) or 0

    @classmethod
    def total_month_revenue(cls, year=None, month=None):

        queryset = cls.objects.all()

        if year:
            queryset = queryset.filter(sale_date__year=year)
        if month:
            queryset = queryset.filter(sale_date__month=month)

        result = queryset.aggregate(
            total_revenue=Sum(F('quantity') * F('batch__price'))
        )
        return result['total_revenue'] or 0

    def __str__(self):
        return str(self.batch)


