import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Sale
from datetime import datetime
import os
from django.db.models import Sum, Avg
from django.utils.dateparse import parse_date
from django.db import connection
import logging


logger = logging.getLogger(__name__)

class HealthCheckView(APIView):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result == (1,):
                    logger.info("Good health check", extra={
                    'endpoint': '/api/health/',
                    'params': request.query_params.dict(),
                    'request_id': getattr(request, 'request_id', 'N/A')
                })
                    return Response({"status": "ok", "database": "reachable"}, status=200)
        except Exception as e:
            logger.error("Health check FAILED", extra={
                'endpoint': '/api/health/',
                'params': {},
                'request_id': getattr(request, 'request_id', 'N/A'),
                'error': str(e)
            })
            return Response({"status": "error", "database": "unreachable", "detail": str(e)}, status=500)

class ImportSalesView(APIView):
    def get(self, request):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'sales.csv')
        imported_rows = 0

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    sale_date = datetime.strptime(row['Sale Date'], '%m/%d/%Y').date()
                    order_id = row['Sale ID']
                    product_id = row['Item name']
                    amount = float(row['Item Total'])

                    Sale.objects.create(
                        date=sale_date,
                        order_id=order_id,
                        product_id=product_id,
                        amount_sgd=amount
                    )
                    imported_rows += 1
                except Exception as e:
                    print(f"Skipping row due to error: {e}")
                    
        logger.info("Imported sales", extra={
            'endpoint': '/api/import-sales/',
            'params': request.query_params.dict(),
            'request_id': getattr(request, 'request_id', 'N/A'),
            'imported_rows': imported_rows
        })
        return Response({'imported_rows': imported_rows}, status=status.HTTP_201_CREATED)

class RevenueMetricsView(APIView):
    def get(self, request):
        """
            Returns total revenue and average order value.
            Query params:
            - start: YYYY-MM-DD
            - end: YYYY-MM-DD
        """
        start = parse_date(request.GET.get('start'))
        end = parse_date(request.GET.get('end'))

        if not start or not end:
            return Response({'error': 'Invalid or missing start/end date.'}, status=400)

        sales = Sale.objects.filter(date__range=(start, end))

        total_revenue = sales.aggregate(total=Sum('amount_sgd'))['total'] or 0
        average_order = sales.aggregate(avg=Avg('amount_sgd'))['avg'] or 0

        logger.info("Queried revenue metrics", extra={
            'endpoint': '/api/metrics/revenue/',
            'params': request.query_params.dict(),
            'request_id': getattr(request, 'request_id', 'N/A'),
            'total_revenue': round(total_revenue, 2),
            'average_order_value': round(average_order, 2)
        })
        
        return Response({
            "total_revenue_sgd": round(total_revenue, 2),
            "average_order_value_sgd": round(average_order, 2)
        })
        
class DailyRevenueMetricsView(APIView):
    def get(self, request):
        start = parse_date(request.GET.get('start'))
        end = parse_date(request.GET.get('end'))

        if not start or not end:
            return Response({'error': 'Invalid or missing start/end date.'}, status=400)

        sales = (
            Sale.objects
            .filter(date__range=(start, end))
            .values('date')
            .annotate(revenue=Sum('amount_sgd'))
            .order_by('date')
        )

        result = [
            {"date": row["date"].isoformat(), "revenue_sgd": round(row["revenue"], 2)}
            for row in sales
        ]

        logger.info("Queried daily revenue metrics", extra={
            'endpoint': '/api/metrics/revenue/daily/',
            'params': request.query_params.dict(),
            'request_id': getattr(request, 'request_id', 'N/A'),
            'days_returned': len(result)
        })
        
        return Response(result)

  
