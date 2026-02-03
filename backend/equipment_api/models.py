from django.db import models

class EquipmentUpload(models.Model):
    filename = models.CharField(max_length=255)
    total_count = models.IntegerField()
    avg_temp = models.FloatField()
    avg_pressure = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)