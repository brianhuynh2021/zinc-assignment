from django.db import models


class Sale(models.Model):
    date = models.DateField()
    order_id = models.CharField(max_length=100)
    amount_sgd = models.DecimalField(max_digits=10, decimal_places=2)
    product_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.order_id}"
