from app import create_app
from datetime import date
from faker import Faker
from unittest.mock import MagicMock, patch
import unittest

fake = Faker()

class TestOrdersEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('auth.decode_token')
    @patch('services.orderService.save')
    def test_create_order(self, mock_save, mock_decode_token):
        mock_decode_token.return_value = 1
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.date = date(2024, 5, 30)
        mock_order.customer_id = 1
        mock_order.products = [1, 2, 3]
        mock_save.return_value = mock_order
        payload = {
            "products": [1, 2, 3]
        }
        headers = {
            "Authorization": "Bearer 12345"
        }
        response = self.app.post('/orders/', json=payload, headers=headers)
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(response.json['id'], mock_order.id)
        mock_decode_token.assert_called_once_with('12345')