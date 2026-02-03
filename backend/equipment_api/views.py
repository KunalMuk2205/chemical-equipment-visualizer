import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import HttpResponse
from .models import EquipmentUpload
from reportlab.pdfgen import canvas

class UploadView(APIView):
    # Requirement: Basic Authentication
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        df = pd.read_csv(file)
        
        stats = {
            "total_count": len(df),
            "avg_temp": round(df['Temperature'].mean(), 2),
            "avg_pressure": round(df['Pressure'].mean(), 2),
            "type_distribution": df['Type'].value_counts().to_dict()
        }

        # Requirement: History Management (Save and keep only last 5)
        EquipmentUpload.objects.create(
            filename=file.name,
            total_count=stats['total_count'],
            avg_temp=stats['avg_temp'],
            avg_pressure=stats['avg_pressure']
        )
        if EquipmentUpload.objects.count() > 5:
            EquipmentUpload.objects.first().delete()

        return Response(stats)

class PDFReportView(APIView):
    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        p = canvas.Canvas(response)
        p.drawString(100, 800, "Chemical Equipment Summary Report")
        p.drawString(100, 780, f"Generated for: {EquipmentUpload.objects.last().filename}")
        p.showPage()
        p.save()
        return response