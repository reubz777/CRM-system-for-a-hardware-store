from django.db import models

class Supplier(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Имя поставщика",
        unique=True
    )
    contact_face = models.CharField(
        max_length=256,
        verbose_name="Имя менеджера"
    )
    telephone = models.CharField(
        max_length=14,
        verbose_name="Контактный телефон"
    )
    email = models.EmailField(
        max_length=256,
        verbose_name="Контактная электронная почта",
        blank=True,
        null=False,
        default="admin@example.com"
    )


    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Поставщик"

