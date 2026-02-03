from django.contrib import admin
from django.urls import path
from equipment_api.views import UploadView # Make sure this matches

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/upload/', UploadView.as_view()), # This is the endpoint the frontend will call
]