from django.contrib import admin
from .models import AnalysisHistory

@admin.register(AnalysisHistory)
class AnalysisHistoryAdmin(admin.ModelAdmin):
    list_display = ('filename', 'avg_temp', 'avg_pressure', 'timestamp')