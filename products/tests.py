from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Product, Price
from decimal import Decimal
from urllib.parse import urlencode

class ProductTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')

        self.product = Product.objects.create(name='Test Product', user=self.user)

        self.price = Price.objects.create(product=self.product,
                                          price=50.00,
                                          start_date=date(2024, 2, 29))

        self.price2 = Price.objects.create(product=self.product,
                                           price=100.00,
                                           start_date=date(2024, 2, 28))

        self.price3 = Price.objects.create(product=self.product,
                                           price=150.00,
                                           start_date=date(2024, 2, 27))

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')

        product_prices = self.product.price.all()
        self.assertTrue(self.price in product_prices)
        self.assertEqual(product_prices[0].price, 150.00)
        self.assertEqual(product_prices[1].price, 100.00)
        self.assertEqual(product_prices[2].price, 50.00)


class ProductPriceAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.product_for_average_test = Product.objects.create(name='Product to test average', user=self.user, id=1)

        Price.objects.create(product=self.product_for_average_test,
                             price=Decimal('25.00'),
                             start_date='2024-02-26')

        Price.objects.create(product=self.product_for_average_test,
                             price=Decimal('50.00'),
                             start_date='2024-02-27')

        Price.objects.create(product=self.product_for_average_test,
                             price=Decimal('100.00'),
                             start_date='2024-02-28')

        Price.objects.create(product=self.product_for_average_test,
                             price=Decimal('150.00'),
                             start_date='2024-02-29')

    def test_login(self):
        url = '/api/v1/api-token-auth/'
        data = {"username": "testuser", "password": "12345"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_create_product(self):
        url = reverse('product-list')
        data = {'name': 'Test Product'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(name=data['name']).name, 'Test Product')

    def test_create_price_for_product(self):
        product = Product.objects.create(name='Test Product 3', user=self.user)

        url = reverse('price-list')
        data = {
            'product': product.id,
            'price': '100.00',
            'start_date': '2024-03-01',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        current_product = Product.objects.get(name='Test Product 3')
        prices = current_product.price.all()

        self.assertEqual(prices.count(), 1)

    def test_average_price(self):
        url = f'/api/v1/prices/{self.product_for_average_test.id}/average_price/'    
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_price'], 81.25)

    def test_average_price_with_range_of_dates(self):
        url = f'/api/v1/prices/{self.product_for_average_test.id}/average_price/'
        data = {
            'from_date': '2024-02-26',
            'to_date': '2024-02-28'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_price'], Decimal('58.33'))

    def test_retrieve_product_with_price_history(self):
        url = reverse('product-detailed-info', kwargs={'pk': self.product_for_average_test.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_name'], 'Product to test average')
        self.assertEqual(response.data['current_price'], Decimal('150.00'))
        self.assertEqual(len(response.data['price_history']), 4)


