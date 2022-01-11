from decimal import Decimal

from django.db import models
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Item(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(verbose_name='Контент')
    sale = models.FloatField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to='shop/', verbose_name='Фото')

    def __str__(self):
        return f'{self.title} Цена : {self.price} Категория : {self.category.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Item, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи'
