from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm


def cart_detail(request):
    """
    View displaying products from the shopping cart
    """

    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            product=item['product'], initial={'override': True})

    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    """
    View used to add products to shopping cart or update quantity products
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    form = CartAddProductForm(request.POST, product=product)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'], update_quantity=cd['override'])

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    View removing products from the cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')
