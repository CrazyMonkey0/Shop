from collections.abc import Iterable
from typing import Any
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    # Reference to the parent category (self-referential)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories') 
    
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category',
                       args=[self.slug])

    def get_ancestors(self):
        """Retrieve all ancestors (the path to the root category)."""
        ancestors = []
        category = self
        while category.parent:
            ancestors.append(category.parent)
            category = category.parent
        return ancestors[::-1] 

    def get_descendants(self):
        """Retrieve all subcategories, including nested ones."""
        descendants = []
        for subcategory in self.subcategories.all():
            descendants.append(subcategory)
            descendants.extend(subcategory.get_descendants())
        return descendants


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
