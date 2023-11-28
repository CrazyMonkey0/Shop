from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    subcategories = None
    categories = Category.objects.filter(parents__isnull=True)
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(
            Category, slug=category_slug)
        # Download all subcategories
        subcategories = category.category_set.all()
        # Create a list of category IDs (along with the ID of the category itself)
        category_ids = [category.id] + list(
            subcategory.id for subcategory in subcategories)
        # Get all products belonging to the selected categories
        products = Product.objects.filter(
            category__id__in=category_ids, available=True)

    return render(request, 'products/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'subcategories': subcategories, })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm(product=product)

    return render(request, 'products/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
