from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', ) 
    list_filter = ('parent',)  
    search_fields = ('name',)  
    prepopulated_fields = {'slug': ('name',)}  

    def get_queryset(self, request):
        """
        Customize the queryset to include all categories sorted by hierarchy.
        """
        queryset = super().get_queryset(request)
        return queryset.order_by('parent__id', 'name')  


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'quantity_available', 'available', 'created', 'updated']
    list_filter = ['available', 'category', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
