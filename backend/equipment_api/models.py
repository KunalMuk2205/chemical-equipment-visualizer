from django.db import models
from django.contrib.auth.models import User

class AnalysisHistory(models.Model):
    filename = models.CharField(max_length=255)
    avg_temp = models.FloatField()
    avg_pressure = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # Corrected the parameter name below:
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.filename} - {self.timestamp}"