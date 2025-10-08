from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import ProductFilter

from store.models import Product
from store.cart.cart import Cart
from .serializers import (
    ProductSerializer,
    CartSerializer,
    CartAddSerializer
)



class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows products to be viewed.
    - GET /api/products/ (List, with pagination/filtering)
    - GET /api/products/{id}/ (Detail)
    """
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['name', 'price']
    ordering = ['name']


class CartAPIView(APIView):
    """
    API endpoint to view, add, or update the cart.
    - GET /api/cart/
    - POST /api/cart/
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart = Cart(request)
        cart_data = {
            'items': [{'product_id': item['product'].id, 'name': item['product'].name, 'price': item['price'],
                       'quantity': item['quantity'], 'total_price': item['total_price']} for item in cart],
            'total_price': cart.get_total_price()
        }
        serializer = CartSerializer(cart_data)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartAddSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            product = get_object_or_404(Product, id=data['product_id'])
            cart = Cart(request)
            cart.add(
                product=product,
                quantity=data['quantity'],
                override_quantity=True
            )

            return Response({'message': 'Item added/updated successfully', 'cart_length': len(cart)},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartRemoveAPIView(APIView):
    """
    DELETE /api/cart/{product_id}/ : Remove a specific item from the cart.
    """
    permission_classes = [permissions.AllowAny]

    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)

        cart.remove(product)

        return Response({'message': 'Item removed successfully', 'cart_length': len(cart)},
                        status=status.HTTP_204_NO_CONTENT)
