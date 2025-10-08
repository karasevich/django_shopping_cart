from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from store.models import Product, Category


# Tests the complete cart CRUD cycle using APITestCase,
# which automatically manages sessions and the test database.

class TestCartAPI(APITestCase):
    """Tests for the Cart API (endpoints: /api/cart/ and /api/cart/<id>/)."""

    def setUp(self):
        """Sets up test data: category and product for cart interaction."""

        # 1. Create Category first (required by Product model)
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category"
        )

        # 2. Create a test product with ID=1, linked to the category.
        self.product = Product.objects.create(
            category=self.category,  # <-- Added required ForeignKey
            name="Test Product",
            slug="test-product",
            price=10.00,
            available=True
        )

        self.add_url = reverse('api_cart_detail_add')  # /api/cart/
        # Helper to dynamically generate the removal URL: /api/cart/<id>/
        self.remove_url = lambda pid: reverse('api_cart_remove', kwargs={'product_id': pid})

        self.add_data_initial = {
            'product_id': self.product.id,
            'quantity': 2,
        }
        self.add_data_update = {
            'product_id': self.product.id,
            'quantity': 5,
        }

    def test_add_and_view_item(self):
        """Tests step 1: Adding an item and receiving a correct GET response."""

        # 1. POST: Add 2 units of the product (initial quantity: 2)
        response_add = self.client.post(self.add_url, self.add_data_initial, format='json')
        self.assertEqual(response_add.status_code, status.HTTP_200_OK)
        self.assertEqual(response_add.data['cart_length'], 2)

        # 2. GET: Check cart status
        response_get = self.client.get(self.add_url)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data['items']), 1)
        self.assertEqual(response_get.data['items'][0]['quantity'], 2)  # Checks that the quantity is 2
        self.assertEqual(response_get.data['total_price'], '20.00')

    def test_update_item_quantity(self):
        """Tests step 2: Updating item quantity (from 2 to 5)."""

        # Step A: Add 2 units
        self.client.post(self.add_url, self.add_data_initial, format='json')

        # Step B: POST with new quantity (5) to trigger update
        response_update = self.client.post(self.add_url, self.add_data_update, format='json')
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)

        # Because override_quantity=True, the total length should be 5, not 7.
        self.assertEqual(response_update.data['cart_length'], 5)

        # Step C: GET to verify the quantity was updated
        response_get = self.client.get(self.add_url)
        self.assertEqual(response_get.data['items'][0]['quantity'], 5)
        self.assertEqual(response_get.data['total_price'], '50.00')

    def test_remove_item(self):
        """Tests step 3: Removing an item and final cart check."""

        # Step A: Add an item
        self.client.post(self.add_url, self.add_data_initial, format='json')

        # Step B: DELETE
        response_remove = self.client.delete(self.remove_url(self.product.id))

        # Status 204 No Content - standard for successful deletion
        self.assertEqual(response_remove.status_code, status.HTTP_204_NO_CONTENT)

        # Step C: Final GET check (cart should be empty)
        response_final = self.client.get(self.add_url)
        self.assertEqual(response_final.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_final.data['items']), 0)
        self.assertEqual(response_final.data['total_price'], '0.00')
