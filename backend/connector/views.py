from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
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

                # Only assign user if authenticated
                user = request.user if request.user.is_authenticated else None
                StoredFile.objects.create(
                    user=user,
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
        # For unauthenticated users or development, return all files
        if not user.is_authenticated:
            return StoredFile.objects.all()
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

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download file data as JSON."""
        file = self.get_object()
        
        try:
            if not os.path.exists(file.filepath):
                return Response(
                    {"error": "File not found on disk"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            with open(file.filepath, 'r') as f:
                data = json.load(f)
            
            return Response(data, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON file"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
def extract_data_endpoint(request):
    """Extract data from a database connection."""
    connection_id = request.data.get('connection_id')
    table_name = request.data.get('table_name')
    
    if not connection_id:
        return Response({"error": "connection_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not table_name:
        return Response({"error": "table_name is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        connection = DatabaseConnection.objects.get(id=connection_id)
        
        for batch in extract_data_in_batches(connection, table_name):
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

            # Only assign user if authenticated
            user = request.user if request.user.is_authenticated else None
            StoredFile.objects.create(
                user=user,
                filepath=filepath
            )
            return Response(batch, status=status.HTTP_200_OK)
        
        return Response({"message": "Extraction complete, but no data found."}, status=status.HTTP_200_OK)

    except DatabaseConnection.DoesNotExist:
        return Response({"error": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
