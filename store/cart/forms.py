from django import forms

class CartAddProductForm(forms.Form):
    """
    Form for adding products to the cart.
    """
    # Quantity field (choices from 1 to 20, for example)
    QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
    quantity = forms.TypedChoiceField(
        choices=QUANTITY_CHOICES,
        coerce=int,  # Convert selected value to integer
        label='Quantity'
    )
    # Field to specify whether to override the quantity or add to the existing one
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )