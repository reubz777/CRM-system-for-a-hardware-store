from django.db import models
from django.db.models import Count, Q

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Имя категории")

    class Meta:
        db_table = "Категории"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name
