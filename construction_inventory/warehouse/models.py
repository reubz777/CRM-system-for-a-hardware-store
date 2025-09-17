from django.db import models
from django.core.validators import MinValueValidator
from products.models import Product
from simple_history.models import HistoricalRecords

class BatchGroup(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='batch_groups',
        verbose_name='Товар'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания группы"
    )

    class Meta:
        db_table = "Группы партий"
        verbose_name = "Группа партий"
        verbose_name_plural = "Группы партий"
        ordering = ['-created_date']

    def __str__(self):
        if self.pk:
            return f"{self.pk}"
        return f"(Группа #{self.pk})"

    @property
    def total_quantity(self):
        return self.batches.aggregate(total=models.Sum('quantity'))['total'] or 0

    def get_active_batches(self):
        return self.batches.filter(quantity__gt=0)


class Batch(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="batches",
        verbose_name="Товар",
    )
    group = models.ForeignKey(
        BatchGroup,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='batches',
        verbose_name='Группа партии',
        editable=False,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена реализации"
    )
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Количество"
    )
    arrival_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата поступления партии",
        editable=False,
    )
    is_modified = models.BooleanField(  # ЗАМЕНА originality
        default=False,
        verbose_name="Измененная партия",
        help_text="Отметьте если партия была изменена",
        editable = False
    )

    history = HistoricalRecords()

    class Meta:
        db_table = "Партии товаров"
        verbose_name = "Партия товара"
        verbose_name_plural = "Партии товаров"
        ordering = ['-arrival_date']

    def __str__(self):
        status = "Измененная" if self.is_modified else "Оригинальная"
        product_name = self.product.name if self.product else "Неизвестный товар"
        return f"Партия #{self.id} - {product_name} - {status}"

    def modify_quantity(self, new_quantity, new_price=None):
        if new_quantity < 0:
            raise ValueError("Количество не может быть отрицательным")

        self.quantity = new_quantity
        if new_price is not None:
            self.price = new_price
        self.is_modified = True
        self.save()
        return self
