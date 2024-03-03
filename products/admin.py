from django.contrib import admin
from .models import Product, Price

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    class Meta:
        model = Product
        fields = '__all__'

admin.site.register(Price)