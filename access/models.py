from django.db import models
from products.models import Product


class ProductAccess(models.Model):

    email = models.EmailField()

    customer_name = models.CharField(max_length=100)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    password = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.product.name}"
