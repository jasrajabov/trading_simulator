from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from w_app.models import TradeData
import ipdb


class TradeDataApiTests(APITestCase):
    """
    Rest Api tests
    """
    def setUp(self):
        self.data1={
            "symbol": 'FB',
            "price": '1',
            "quantity": '23',
            "order_type": 'Market',
            "direction": 'Sell',
            }
        self.data2={
            "symbol": 'FB',
            "price": '1',
            "quantity": '23',
            "order_type": 'Market',
            "direction": 'Buy',
            }
        # url = 'http://localhost:8000/trades/'
        self.url = reverse('trades')
    def test_trade_booking(self):
        """
        Test trade is booked successfully
        """
        response = self.client.post(self.url, self.data1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TradeData.objects.count(), 1)
        self.assertIsNotNone(TradeData.objects.get().fix)

    def test_get_all_trades(self):
        """
        Test get all trades work
        """
        self.client.post(self.url, self.data1)
        self.client.post(self.url, self.data2)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TradeData.objects.count(), 2)
        self.assertEqual(TradeData.objects.filter(id=1).get().direction, 'Sell')
