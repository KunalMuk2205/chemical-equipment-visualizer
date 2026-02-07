import pandas as pd
import io
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import AnalysisHistory

@api_view(['POST', 'GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def upload_file(request):
    # --- HANDLE PDF DOWNLOAD (GET REQUEST) ---
    if request.method == 'GET' and request.query_params.get('export') == 'pdf':
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        
        # Draw Header
        p.setFont("Helvetica-Bold", 18)
        p.setStrokeColorRGB(0.2, 0.5, 0.9)
        p.drawString(100, 750, "CHEMICAL EQUIPMENT ANALYSIS REPORT")
        p.line(100, 745, 500, 745)
        
        # Draw Body
        p.setFont("Helvetica", 12)
        p.drawString(100, 710, f"Analyst: {request.user.username}")
        p.drawString(100, 690, "Summary: The latest dataset has been processed successfully.")
        p.drawString(100, 670, "Please refer to the digital dashboard for live distribution charts.")
        
        p.showPage()
        p.save()
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Analysis_Report.pdf"'
        return response

    # --- HANDLE FILE UPLOAD (POST REQUEST) ---
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=400)

        file = request.FILES['file']
        df = pd.read_csv(file)
        
        # 1. Intelligence: Calculate Stats & Outliers
        avg_temp = round(float(df['Temperature'].mean()), 2)
        avg_press = round(float(df['Pressure'].mean()), 2)
        
        # Outlier detection (Flag if temp > 100 as a simple example)
        outliers = df[df['Temperature'] > 100]
        outlier_count = len(outliers)

        stats = {
            "total_count": int(len(df)),
            "avg_temp": avg_temp,
            "avg_pressure": avg_press,
            "type_distribution": df['Type'].value_counts().to_dict(),
            "outlier_alerts": outlier_count,
            "status": "Warning" if outlier_count > 0 else "Normal"
        }

        # 2. Save to Database
        AnalysisHistory.objects.create(
            filename=file.name,
            avg_temp=avg_temp,
            avg_pressure=avg_press,
            user=request.user
        )
        
        return Response(stats)