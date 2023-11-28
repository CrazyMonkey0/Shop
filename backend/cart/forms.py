from django import forms


class CartAddProductForm(forms.Form):
    """
    A form for adding products to a shopping cart
    """

    override = forms.BooleanField(required=False, initial=False,
                                  widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        # Get the product from the arguments (if available)q
        product = kwargs.pop('product', None)
        super(CartAddProductForm, self).__init__(*args, **kwargs)

        # Set the available quantities in the quantity field
        if product:
            # Limit to 20 if quantity_available is greater
            max_quantity = min(product.quantity_available, 20)
            # Create a list of available options based on quantity_available
            choices = [(i, str(i)) for i in range(1, max_quantity + 1)]
            self.fields['quantity'] = forms.TypedChoiceField(
                choices=choices,
                empty_value=0,
                coerce=int, label=('Quantity'), initial=0
            )
