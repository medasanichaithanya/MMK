from django.test import TestCase, Client
from django.urls import reverse
import json

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_apiOne(self):
        url = reverse('apiOne')
        data = {
            'to': '1234567890',
            'from': '9876543210',
            'text': 'Hello, World!'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 403)
       

    def test_apiTwo(self):
        url = reverse('apiTwo')
        data = {
            'to': '1234567890',
            'from': '9876543210',
            'text': 'Hello, World!'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        # Assert the expected response content