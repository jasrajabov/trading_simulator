from django.db import models

class TradeData(models.Model):
    fix = models.CharField(max_length=200)
    symbol = models.CharField(max_length=20)
    quantity = models.CharField(max_length=20)
    order_type = models.CharField(max_length=20)
    direction = models.CharField(max_length=20)
    exec_date = models.DateTimeField()
