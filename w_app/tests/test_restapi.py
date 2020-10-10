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
        # ipdb.set_trace()
        response = self.client.post(self.url, self.data1)
        # ipdb.set_trace()
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
        # ipdb.set_trace()
        self.assertEqual(TradeData.objects.filter(id=response.data[0]['id']).get().direction, 'Sell')

    # def test_post_single_trade(self):
    #     """testing fetching a single trade"""
    #     url = reverse('single_trade', kwargs={'id':'1'})
    #     # ipdb.set_trace()
    #     response = self.client.post(url, self.data1)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_trade(self):
        """testing fetching a single trade"""
        trade = self.client.post(self.url, self.data1)
        url = reverse('single_trade', kwargs={'id':trade.data['id'].__str__()})
        # ipdb.set_trace()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_single_trade(self):
        trade = self.client.post(self.url, self.data1)
        url = reverse('single_trade', kwargs={'id':trade.data['id'].__str__()})
        # ipdb.set_trace()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TradeData.objects.count(), 0)
