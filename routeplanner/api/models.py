from django.db import models

from django.db import models

class FuelPrice(models.Model):
    truckstop_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    retail_price = models.FloatField()

    def __str__(self):
        return f"{self.truckstop_name} ({self.city}, {self.state})"


