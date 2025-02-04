from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product
from cart.forms import CartAddProductForm



def product_list(request, category_slug=None):
    categories = Category.objects.filter(parent__isnull=True) 
    products = Product.objects.filter(available=True)
    category = None
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        descendant_ids = [descendant.id for descendant in category.get_descendants()]
        category_ids = [category.id] + descendant_ids
        products = Product.objects.filter(category__id__in=category_ids, available=True)

    paginator = Paginator(products, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'page_obj': page_obj
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm(product=product)

    return render(request, 'products/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
