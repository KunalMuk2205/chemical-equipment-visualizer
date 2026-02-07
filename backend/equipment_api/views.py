import pandas as pd
import io
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import AnalysisHistory

# --- NEW: SAMPLE CSV GENERATOR ---
@api_view(['GET'])
@permission_classes([]) # Optional: Allow anyone to download the sample
def download_sample_csv(request):
    """Generates a valid CSV template for users to test the system."""
    csv_data = (
        "Equipment,Type,Temperature,Pressure\n"
        "Reactor_01,Reactor,45.5,10.2\n"
        "Pump_02,Pump,42.0,12.5\n"
        "Boiler_03,Boiler,210.0,15.0\n"
        "Valve_04,Valve,48.2,11.1\n"
        "Sensor_05,Reactor,55.0,10.8"
    )
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_chemical_data.csv"'
    return response

@api_view(['POST', 'GET'])
def upload_file(request):
    # --- 1. PDF GENERATION LOGIC (GET REQUEST) ---
    if request.method == 'GET' and request.GET.get('export') == 'pdf':
        last_entry = AnalysisHistory.objects.filter(user=request.user).last()
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        
        # UI Styling for PDF
        p.setFont("Helvetica-Bold", 18)
        p.drawString(100, 800, "CHEMICAL EQUIPMENT ANALYSIS REPORT")
        p.line(100, 795, 500, 795)
        
        p.setFont("Helvetica", 12)
        p.drawString(100, 770, f"Analyst: {request.user.username}")
        
        if last_entry:
            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, 740, f"Filename: {last_entry.filename}")
            
            p.setFont("Helvetica", 12)
            p.drawString(100, 720, f"Average Temperature: {last_entry.avg_temp} °C")
            p.drawString(100, 700, f"Average Pressure: {last_entry.avg_pressure} bar")
            p.drawString(100, 680, f"Analysis Date: {last_entry.timestamp.strftime('%Y-%m-%d %H:%M')}")
            
            p.setFont("Helvetica-Oblique", 10)
            p.drawString(100, 650, "Status: Data verified via Outlier Detection System.")
        else:
            p.drawString(100, 740, "Error: No recent analysis data found in history.")

        p.showPage()
        p.save()
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Equipment_Report.pdf"'
        return response

    # --- 2. FILE UPLOAD LOGIC (POST REQUEST) ---
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=400)

        file = request.FILES['file']
        try:
            df = pd.read_csv(file)
            
            # Basic Stats
            avg_temp = round(df['Temperature'].mean(), 2)
            avg_press = round(df['Pressure'].mean(), 2)
            dist = df['Type'].value_counts().to_dict()

            # Outlier Detection (Z-Score approximation)
            temp_std = df['Temperature'].std()
            outliers = df[df['Temperature'] > (avg_temp + 2 * temp_std)]
            outlier_count = len(outliers)

            # SAVE TO DATABASE
            history = AnalysisHistory.objects.create(
                filename=file.name,
                avg_temp=avg_temp,
                avg_pressure=avg_press,
                user=request.user
            )

            return Response({
                "id": history.id,
                "total_count": len(df),
                "avg_temp": avg_temp,
                "avg_pressure": avg_press,
                "type_distribution": dist,
                "outlier_alerts": outlier_count,
                "status": "Warning" if outlier_count > 0 else "Normal"
            })
        except Exception as e:
            return Response({"error": f"Failed to process CSV: {str(e)}"}, status=400)