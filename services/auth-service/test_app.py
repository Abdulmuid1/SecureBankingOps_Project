import unittest
import json
from app import app # Imports the flask app from app.py

class TestService(unittest.TestCase):
    
    def setUp(self):
        # Create a test client (mock browser)
        self.client = app.test_client()
        self.client.testing = True 

    def test_health_check(self):
        """
        Since every service has /health, this tests if the app is alive.
        """
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "OK")

    def test_404_route(self):
        """
        Tests that a fake URL returns 404 (Standard for all apps)
        """
        response = self.client.get('/this-does-not-exist')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()