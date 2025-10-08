from django.db import models
from django.urls import reverse

class Category(models.Model):
    """
    Product categories model.
    """
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        """Returns the category name."""
        return self.name

    def get_absolute_url(self):
        """Returns the URL for the category filtered list."""
        return reverse('store:product_list_by_category', args=[self.slug])

class Product(models.Model):
    """
    Product item model.
    """
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def __str__(self):
        """Returns the product name."""
        return self.name

    def get_absolute_url(self):
        """Returns the URL for a specific product detail view."""
        return reverse('store:product_detail', args=[self.id, self.slug])
