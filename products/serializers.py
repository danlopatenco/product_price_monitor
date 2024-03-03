from rest_framework import serializers
from .models import Product, Price
from django.utils.timezone import now


class ProductSerializer(serializers.ModelSerializer):
    initial_price = serializers.DecimalField(max_digits=10,
                                             decimal_places=2,
                                             write_only=True,
                                             required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'initial_price']

    def create(self, validated_data):
        initial_price = validated_data.pop('initial_price', None)
        product = super().create(validated_data)
        if initial_price is not None:
            Price.objects.create(product=product, price=initial_price, start_date=now().date())
        return product


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['id', 'product', 'price', 'start_date', 'end_date']