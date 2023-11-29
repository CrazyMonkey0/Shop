from django.shortcuts import render
from cart.cart import Cart
from .tasks import order_created
from .forms import OrderCreateForm
from .models import OrderItem


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                if item['product'].quantity_available > 0:
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                # Remove the contents of the shopping cart
            cart.clear()
            order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html',
                      {'cart': cart, 'form': form})
