from django.urls import path
from .views import (ImportSalesView, RevenueMetricsView, DailyRevenueMetricsView,
                    HealthCheckView)

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('import-sales/', ImportSalesView.as_view(), name='import-sales'),
    path('metrics/revenue/', RevenueMetricsView.as_view(), name='revenue-metrics'),
    path('metrics/revenue/daily/', DailyRevenueMetricsView.as_view(), name='daily-revenue-metrics'),
]