from django.db import models

class AnalysisHistory(models.Model):
    filename = models.CharField(max_length=255)
    avg_temp = models.FloatField()
    avg_pressure = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} - {self.timestamp}"