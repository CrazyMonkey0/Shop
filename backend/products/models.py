from collections.abc import Iterable
from typing import Any
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    parents = models.ForeignKey(
        'self', related_name='category_set', null=True, blank=True,
        on_delete=models.CASCADE, limit_choices_to={'parents__isnull': True})

    class Meta:
        ordering = ('name',)
        # Defines the human-readable name of the model in singular.
        verbose_name = 'category'
        # Defines the human-readable plural name of the model.
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail',
                       args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        # Update the 'available' field based on 'quantity_available'
        self.available = self.quantity_available > 0
        return super(Product, self).save(*args, **kwargs)
