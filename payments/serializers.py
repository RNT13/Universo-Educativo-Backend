from rest_framework import serializers
from products.models import Product


class CheckoutSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    customer_name = serializers.CharField()
    email = serializers.EmailField()

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Produto não encontrado.")
        return value
