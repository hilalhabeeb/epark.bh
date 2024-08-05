from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class ParkingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20)
    parking_location = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=0.100)  # Default amount 100 fills

    def save(self, *args, **kwargs):
        if not self.end_time:
            self.end_time = self.start_time + timedelta(hours=2)  # Default parking duration is 2 hours
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.vehicle_number} at {self.parking_location}'
