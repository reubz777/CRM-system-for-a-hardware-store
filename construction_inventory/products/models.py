from django.db import models
from supplies.models import Supplier
from categories.models import Category

class Product(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="Имя продукта")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Категория"
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Поставщик"
    )    


    class Meta:
        db_table = "Товары"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return str(self.name)

    @property
    def total_quantity(self):
        return self.batches.aggregate(total=models.Sum('quantity'))['total'] or 0


