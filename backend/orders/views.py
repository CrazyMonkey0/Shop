from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from cart.cart import Cart
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from django.core.cache import cache
from decimal import Decimal
from .forms import OrderCreateForm
from .models import OrderItem, Order
import json
import os



class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
    

def paid_order(request, id):
    order = get_object_or_404(Order, id=id)

    if order.paid:
        return render(request, 'orders/order/paid.html', {'order': order} )   
    else:
        return render(request, 'orders/order/paid.html', {'order': order} )
    

def request_to_payment_gateway(request):
    if request.method == 'POST':
        # Get order data from session
        data = json.loads(request.session.get('data', '{}'))
        
        # redirect to payment gateway if order link is available
        if request.session.get('order_link'):
            return redirect(f'{request.session.get("order_link")}')

        # Create OAuth2 session
        client_id = os.getenv('CLIENT_ID')
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)

        # Get access token from cache
        access_token = cache.get('access_token')
        
        #  post request to payment gateway 
        # Verify use only in dev mode
        response = oauth.post(
            'https://web:8000/api/orders/',
            json=data,
            headers={'Authorization': f'Bearer {access_token}'},
            verify=False
        )

        if response.status_code == 201:
            request.session['order_link'] = response.json().get("order_link")
            return redirect(f"{response.json().get('order_link')}")
        else:
            order = get_object_or_404(Order, id=data.get('order_id'))
            return render(request, 'orders/order/payments.html', {
                'order': order,
                'requests': request.session.get('data'),
            })


def order_create(request):
    cart = Cart(request)
    data = {}
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            check_data = json.loads(request.session.get('data', '{}'))
            if check_data.get('order_id'):
                order = get_object_or_404(Order, id=check_data.get('order_id'))
                order.name = form.cleaned_data['name']
                order.surname = form.cleaned_data['surname']
                order.email = form.cleaned_data['email']
                order.address = form.cleaned_data['address']
                order.postal_code = form.cleaned_data['postal_code']
                order.city = form.cleaned_data['city']
            else:
                order = form.save()
        
            data['client'] = {
                "name": order.name,
                "surname": order.surname,
                "email": order.email
            }
            products = []

            for item in cart:
                if item['product'].quantity_available > 0:
                    # Add order item to the database
                    existing_order_item = OrderItem.objects.filter(order=order, product=item['product']).first()
                    if existing_order_item:
                        existing_order_item.quantity = item['quantity']
                        existing_order_item.save()
                    elif item['price'] == 0:
                        pass
                    else:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            price=item['price'],
                            quantity=item['quantity']
                        )
                    products.append({
                        "name": item['product'].name,
                        "quantity": item['quantity']
                    })

            data['products'] = products
            data['order_id'] = str(order.id)
            data['total'] = str(cart.get_total_price())

            # Save data in session
            request.session['data'] = json.dumps(data)
            return render(request, 'orders/order/payments.html', {
                'data': data,
                'order': order,
                'cart': cart,
            })

        else:
            return render(request, 'orders/order/create.html', {
                'cart': cart,
                'form': form
            })

    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {
            'cart': cart,
            'form': form
        })


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})