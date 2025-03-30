from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование продукта")
    description = models.TextField(max_length=250, verbose_name="Описание продукта")
    catalog_image = models.ImageField(upload_to="images/", blank=True, null=True)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        blank=True,
        null=True,
        related_name="products",
    )
    cost = models.IntegerField(verbose_name="Цена за покупку")
    created_at = models.DateField(verbose_name="Дата создания")
    updated_at = models.DateField(verbose_name="Дата последнего изменения")
    objects = models.Manager()

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование категории")
    description = models.TextField(max_length=250, verbose_name="Описание категории", blank=True, null=True)
    objects = models.Manager()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name
