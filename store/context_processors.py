from .cart.cart import Cart
from .models import Category


def global_context(request):
    """
    Context processor to make the cart object and all categories available
    to all templates.
    """
    cart = Cart(request)
    categories = Category.objects.all()

    return {
        'cart': cart,
        'categories': categories,
    }