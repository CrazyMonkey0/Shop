from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart(object):
    def __init__(self, request) -> None:
        """
        Initializing the shopping cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # Save an empty shopping cart for the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        """
        Save session cart
        """
        # Mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def add(self, product, quantity=1, update_quantity=False):
        """
        Adding a product to the cart or changing its quantity
        """
        product_id = product.id

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        Removing a product from the shopping cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """
        Calculates the total value of all products in the shopping cart
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Removing the shopping cart from the session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        """
        Iterate through shopping cart items and retrieve products from the database
        """
        product_ids = self.cart.keys()
        # Download product objects and add them to the shopping cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Calculating the number of all items in a shopping cart
        """
        return sum(item['quantity'] for item in self.cart.values())
