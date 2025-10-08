from rest_framework import serializers
from store.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    Includes category name for better readability.
    """
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'image', 'available', 'category']



class CartItemSerializer(serializers.Serializer):
    """
    Serializer for displaying an item in the cart.
    Since cart items are session-based, this uses a base Serializer.
    """
    # Product details are passed as a nested object
    product_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200, read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


class CartSerializer(serializers.Serializer):
    """
    Serializer for displaying the entire cart contents.
    """
    items = CartItemSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartAddSerializer(serializers.Serializer):
    """
    Serializer for validating POST data when adding a product to the cart.
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    override_quantity = serializers.BooleanField(required=False, default=False)

    def validate_product_id(self, value):
        """
        Check if the product exists and is available.
        """
        try:
            Product.objects.get(id=value, available=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or not available.")
        return value