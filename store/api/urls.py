from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', views.CartAPIView.as_view(), name='api_cart_detail_add'),
    path('cart/<int:product_id>/', views.CartRemoveAPIView.as_view(), name='api_cart_remove'),
]