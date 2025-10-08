from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('', views.product_list, name='product_list'),
    path('<int:id>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
]