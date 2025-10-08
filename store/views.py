from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Category, Product
from .cart.cart import Cart
from .cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    """
    Displays the list of products, handling category filtering and pagination.

    Args:
        request: HttpRequest object.
        category_slug: Slug of the category for filtering (optional).
    """
    categories = Category.objects.all()
    current_category = None
    products = Product.objects.filter(available=True)

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    paginator = Paginator(products, 6)  # 6 products per page
    page_number = request.GET.get('page', 1)

    try:
        products_page = paginator.page(page_number)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    context = {
        'current_category': current_category,
        'categories': categories,
        'products': products_page,
    }
    return render(request, 'store/product/list.html', context)


def product_detail(request, id, product_slug):
    """
    Displays the detail page for a single product.

    Args:
        request: HttpRequest object.
        id: Product ID.
        product_slug: Product slug (for SEO, consistency check).
    """
    product = get_object_or_404(Product,
                                id=id,
                                slug=product_slug,
                                available=True)

    cart_product_form = CartAddProductForm()

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'current_category': product.category
    }
    return render(request, 'store/product/detail.html', context)


@require_POST
def cart_add(request, product_id):
    """
    Handles adding a product to the cart or updating its quantity.
    Requires POST method.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )

    return redirect('store:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    Removes a product from the cart.
    Requires POST method.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('store:cart_detail')


def cart_detail(request):
    """
    Displays the contents of the shopping cart.
    """
    cart = Cart(request)

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True
            }
        )

    return render(request, 'store/cart/detail.html', {'cart': cart})