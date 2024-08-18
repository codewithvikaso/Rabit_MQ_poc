from django.db import models

# Create your models here.

class StatusMessage(models.Model):
    status = models.IntegerField()
    timestamp = models.FloatField()

    def __str__(self):
        return f"Status: {self.status}, Timestamp: {self.timestamp}"