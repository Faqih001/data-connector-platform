from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import DatabaseConnection, StoredFile, ExtractedData
from .serializers import DatabaseConnectionSerializer, StoredFileSerializer, ExtractedDataSerializer
from .services import extract_data_in_batches
import json
import os
from django.conf import settings
from datetime import datetime

class DatabaseConnectionViewSet(viewsets.ModelViewSet):
    queryset = DatabaseConnection.objects.all()
    serializer_class = DatabaseConnectionSerializer

    @action(detail=True, methods=['post'])
    def extract_data(self, request, pk=None):
        connection = self.get_object()
        table_name = request.data.get('table_name')
        if not table_name:
            return Response({"error": "table_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # In a real app, this would be a background task
            for batch in extract_data_in_batches(connection, table_name):
                # For simplicity, we'll just store the first batch as a file
                # and return it. A real implementation would handle all batches.
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"extraction_{connection.name}_{table_name}_{timestamp}.json"
                filepath = os.path.join(settings.MEDIA_ROOT, filename)
                
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                with open(filepath, 'w') as f:
                    json.dump(batch, f, default=str)

                ExtractedData.objects.create(
                    connection=connection,
                    data=batch
                )

                StoredFile.objects.create(
                    user=request.user,
                    filepath=filepath
                )
                return Response(batch, status=status.HTTP_200_OK)
            
            return Response({"message": "Extraction complete, but no data found."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StoredFileViewSet(viewsets.ModelViewSet):
    serializer_class = StoredFileSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'admin':
            return StoredFile.objects.all()
        if user.is_staff: # fallback for default admin user
            return StoredFile.objects.all()
        return StoredFile.objects.filter(user=user) | StoredFile.objects.filter(shared_with=user).distinct()

    @action(detail=True, methods=['post'])
    def submit_data(self, request, pk=None):
        file = self.get_object()
        data = request.data.get('data')

        if not data:
            return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with open(file.filepath, 'w') as f:
                json.dump(data, f, default=str)
            
            return Response({"message": "File updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

