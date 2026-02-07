from django.contrib import admin
from django.urls import path
from equipment_api.views import upload_file, download_sample_csv  # Added download_sample_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Endpoint for uploading CSVs and generating PDF reports
    path('api/upload/', upload_file, name='upload_file'), 
    
    # Endpoint to download the template CSV for testing
    path('api/sample/', download_sample_csv, name='sample_csv'),
]