import unittest
from app import create_app
import json
import re


class AmountTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def get_api_headers(self):
        return {
            'Accept' : 'application/json',
            'Content-Type': 'application/json'
            }

    def test_amount_not_available_400(self):
        response = self.client.get(
            '/api/v1/2020-01-10/USD/JPY?',
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 400)

    def test_amount_not_quantity_400(self):
        response = self.client.get(
            '/api/v1/2020-01-10/USD/JPY?amount=xxx',
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 400)
        
    def test_malformed_reference_date_400(self):
        response = self.client.get(
            '/api/v1/20-20-20/USD/JPY?amount=12.0',
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 400)
        
    def test_currency_code_404(self):
        response = self.client.get(
            '/api/v1/2020-01-10/XYZ/JPY?amount=12.0',
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            '/api/v1/2020-01-10/USD/XYZ?amount=12.0',
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 404)

    def test_reference_date_404(self):
        response = self.client.get(
            '/api/v1/2011-01-10/USD/JPY?amount=12.0',
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 404)
        
    def test_code_200(self):
        response = self.client.get(
            '/api/v1/2020-01-10/JPY/USD?amount=123.1234',
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['currency'], 'JPY')
        self.assertEqual(json_response['amount'], '13499.06')
        response = self.client.get(
            '/api/v1/2020-01-10/USD/JPY?amount=13499.06',
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))        
        self.assertEqual(json_response['currency'], 'USD')
        self.assertEqual(json_response['amount'], '123.1234')
