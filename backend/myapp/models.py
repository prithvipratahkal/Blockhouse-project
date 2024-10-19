from django.db import models

# Create your models here.

class AaplStockData(models.Model):
    time = models.DateTimeField(primary_key=True)  # Maps to TIMESTAMPTZ
    open_price = models.DecimalField(max_digits=20, decimal_places=4)  # Maps to DECIMAL
    close_price = models.DecimalField(max_digits=20, decimal_places=4)  # Maps to DECIMAL
    high_price = models.DecimalField(max_digits=20, decimal_places=4)  # Maps to DECIMAL
    low_price = models.DecimalField(max_digits=20, decimal_places=4)   # Maps to DECIMAL
    volume = models.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        db_table = 'aapl_stock_data'