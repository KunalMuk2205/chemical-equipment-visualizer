import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

class UploadView(APIView):
    def post(self, request):
        file = request.FILES['file']
        df = pd.read_csv(file)
        
        # Simple math using Pandas
        stats = {
            "total_count": int(len(df)),
            "avg_temp": float(df['Temperature'].mean()),
            "avg_pressure": float(df['Pressure'].mean()),
            "type_distribution": df['Type'].value_counts().to_dict(),
            "data": df.to_dict(orient='records')
        }
        return Response(stats)