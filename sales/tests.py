from django.test import TestCase
from rest_framework.test import APIClient
from sales.models import Sale
from datetime import date

class SalesEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Seed test data
        Sale.objects.create(date=date(2025, 3, 1), order_id="A001", product_id="Shoes", amount_sgd=100)
        Sale.objects.create(date=date(2025, 3, 1), order_id="A002", product_id="Hat", amount_sgd=50)
        Sale.objects.create(date=date(2025, 3, 2), order_id="A003", product_id="Socks", amount_sgd=25)

    def test_health_check(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')

    def test_revenue_metrics(self):
        response = self.client.get('/api/metrics/revenue/?start=2025-03-01&end=2025-03-02')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_revenue_sgd'], 175.0)
        self.assertAlmostEqual(response.json()['average_order_value_sgd'], 58.33, places=2)

    def test_daily_revenue_metrics(self):
        response = self.client.get('/api/metrics/revenue/daily/?start=2025-03-01&end=2025-03-02')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data[0]['date'], '2025-03-01')
        self.assertEqual(data[0]['revenue_sgd'], 150.0)
        self.assertEqual(data[1]['date'], '2025-03-02')
        self.assertEqual(data[1]['revenue_sgd'], 25.0)

    def test_import_sales(self):
        # Temporarily copy sales.csv into a test location if needed
        response = self.client.get('/api/import-sales/')
        self.assertEqual(response.status_code, 201)
        self.assertIn('imported_rows', response.json())