import pandas as pd
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from reportlab.pdfgen import canvas # Remember to: pip install reportlab

from .models import AnalysisHistory  # Add this at the top

# Inside your post method, after calculating stats:
AnalysisHistory.objects.create(
    filename=file.name,
    avg_temp=stats['avg_temp'],
    avg_pressure=stats['avg_pressure']
)

class UploadView(APIView):
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=400)

        file = request.FILES['file']
        df = pd.read_csv(file)
        
        # Calculate Stats
        stats = {
            "total_count": int(len(df)),
            "avg_temp": round(float(df['Temperature'].mean()), 2),
            "avg_pressure": round(float(df['Pressure'].mean()), 2),
            "type_distribution": df['Type'].value_counts().to_dict(),
        }

        # If URL has ?download=pdf, return PDF instead of JSON
        if request.query_params.get('download') == 'pdf':
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer)
            p.drawString(100, 800, "FOSSEE Chemical Equipment Report")
            p.drawString(100, 780, f"Total Units: {stats['total_count']}")
            p.drawString(100, 760, f"Avg Temp: {stats['avg_temp']} C")
            p.drawString(100, 740, f"Avg Pressure: {stats['avg_pressure']} bar")
            p.showPage()
            p.save()
            buffer.seek(0)
            return HttpResponse(buffer, content_type='application/pdf')
        
        return Response(stats)