from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from cart.cart import Cart
from .tasks import order_created
from .forms import OrderCreateForm
from .models import OrderItem, Order


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


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})
