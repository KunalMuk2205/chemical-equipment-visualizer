import pandas as pd
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from reportlab.pdfgen import canvas 
from .models import AnalysisHistory 

class UploadView(APIView):
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=400)

        file = request.FILES['file']
        df = pd.read_csv(file)
        
        # 1. Calculate Stats
        stats = {
            "total_count": int(len(df)),
            "avg_temp": round(float(df['Temperature'].mean()), 2),
            "avg_pressure": round(float(df['Pressure'].mean()), 2),
            "type_distribution": df['Type'].value_counts().to_dict(),
        }

        # 2. Save to Database History
        AnalysisHistory.objects.create(
            filename=file.name,
            avg_temp=stats['avg_temp'],
            avg_pressure=stats['avg_pressure']
        )

        # 3. Check for PDF request
        if request.query_params.get('download') == 'pdf':
            return self.generate_pdf(stats)
        
        return Response(stats)

    # THIS IS THE GENERATE PDF FUNCTION
    def generate_pdf(self, stats):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, "FOSSEE Chemical Equipment Report")
        p.setFont("Helvetica", 12)
        p.drawString(100, 770, f"Total Units analyzed: {stats['total_count']}")
        p.drawString(100, 750, f"Average Temperature: {stats['avg_temp']} C")
        p.drawString(100, 730, f"Average Pressure: {stats['avg_pressure']} bar")
        p.showPage()
        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')