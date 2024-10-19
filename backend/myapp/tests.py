from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from myapp.models import AaplStockData
import decimal
import datetime

# Create your tests here.

class BackTestAPITestCase(APITestCase):

    def test_missing_parameters(self):
        """
        Test that the API returns 400 Bad Request when any parameters are missing.
        """
        url = reverse('back_test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_non_numeric_parameters(self):
        """
        Test that the API returns 400 Bad Request when any parameters are non-numeric.
        """
        url = reverse('back_test')
        params = {
            'investing_amount': 'abc',
            'sell_period': 'def',
            'buy_period': 'ghi',
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_parameters(self):
        """
        Test that the API returns 400 Bad Request when any parameters are negative.
        """
        url = reverse('back_test')
        params = {
            'investing_amount': '-10000',
            'sell_period': '-5',
            'buy_period': '-10',
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_parameters(self):
        """
        Test that the API returns 200 OK when valid parameters are provided.
        """
        # Create sample stock data
        dates = [timezone.now() - datetime.timedelta(days=i) for i in range(30)]
        for date in dates:
            AaplStockData.objects.create(
                time=date,
                open_price=decimal.Decimal('100.00'),
                close_price=decimal.Decimal('105.00'),
                high_price=decimal.Decimal('110.00'),
                low_price=decimal.Decimal('95.00'),
                volume=decimal.Decimal('1000')
            )

        url = reverse('back_test')
        params = {
            'investing_amount': '10000',
            'sell_period': '5',
            'buy_period': '10',
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('profit', response.data)
        self.assertIn('events', response.data)
