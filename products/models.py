from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    file_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name
