from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .models import DatabaseConnection, StoredFile, ExtractedData
from .serializers import DatabaseConnectionSerializer, StoredFileSerializer, ExtractedDataSerializer
from .services import extract_data_in_batches, json_to_csv
import json
import os
from django.conf import settings
from datetime import datetime

class DatabaseConnectionViewSet(viewsets.ModelViewSet):
    queryset = DatabaseConnection.objects.all()
    serializer_class = DatabaseConnectionSerializer

    @action(detail=True, methods=['post'])
    def extract_data(self, request, pk=None):
        """Extract data with configurable batch_size and format"""
        connection = self.get_object()
        table_name = request.data.get('table_name')
        batch_size = request.data.get('batch_size', 1000)
        format_type = request.data.get('format', 'json')  # 'json' or 'csv'
        
        if not table_name:
            return Response({"error": "table_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if format_type not in ['json', 'csv']:
            return Response({"error": "format must be 'json' or 'csv'"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # In a real app, this would be a background task
            for batch in extract_data_in_batches(connection, table_name, batch_size=batch_size):
                # Store the first batch as a file
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                file_ext = 'csv' if format_type == 'csv' else 'json'
                filename = f"extraction_{connection.name}_{table_name}_{timestamp}.{file_ext}"
                filepath = os.path.join(settings.MEDIA_ROOT, filename)
                
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                # Save file in requested format
                with open(filepath, 'w') as f:
                    if format_type == 'csv':
                        csv_data = json_to_csv(batch)
                        f.write(csv_data)
                    else:
                        json.dump(batch, f, default=str)

                # Create ExtractedData record (always store JSON in DB)
                extracted_data = ExtractedData.objects.create(
                    connection=connection,
                    data=batch
                )

                # Create StoredFile record linked to ExtractedData
                user = request.user if request.user.is_authenticated else None
                StoredFile.objects.create(
                    user=user,
                    extracted_data=extracted_data,
                    filepath=filepath,
                    format_type=format_type
                )
                return Response({
                    "data": batch,
                    "extracted_data_id": extracted_data.id,
                    "format": format_type,
                    "batch_size": batch_size
                }, status=status.HTTP_200_OK)
            
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
        """Submit modified data with DRF validation and model updates"""
        file = self.get_object()
        data = request.data.get('data')

        if not data:
            return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # ✅ Update ExtractedData model with new data
            if file.extracted_data:
                extracted_data = file.extracted_data
                extracted_data.data = data
                extracted_data.save()
                
                # ✅ Validate via serializer
                serializer = ExtractedDataSerializer(extracted_data)
                validated_data = serializer.data
            else:
                # Fallback: create new ExtractedData if not linked
                extracted_data = ExtractedData.objects.create(
                    connection=file.extracted_data.connection if file.extracted_data else None,
                    data=data
                )
                file.extracted_data = extracted_data
                file.save()
                serializer = ExtractedDataSerializer(extracted_data)
                validated_data = serializer.data

            # Save to disk file (backup)
            file_ext = 'csv' if file.format_type == 'csv' else 'json'
            with open(file.filepath, 'w') as f:
                if file.format_type == 'csv':
                    csv_data = json_to_csv(data)
                    f.write(csv_data)
                else:
                    json.dump(data, f, default=str)
            
            # ✅ Return validated data and success
            return Response({
                "message": "Data updated successfully",
                "extracted_data": validated_data,
                "updated_at": extracted_data.updated_at
            }, status=status.HTTP_200_OK)
        
        except ExtractedData.DoesNotExist:
            return Response({"error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)
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
    """Extract data from a database connection with batch_size and format support."""
    connection_id = request.data.get('connection_id')
    table_name = request.data.get('table_name')
    batch_size = request.data.get('batch_size', 1000)
    format_type = request.data.get('format', 'json')
    
    if not connection_id:
        return Response({"error": "connection_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not table_name:
        return Response({"error": "table_name is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if format_type not in ['json', 'csv']:
        return Response({"error": "format must be 'json' or 'csv'"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        connection = DatabaseConnection.objects.get(id=connection_id)
        
        for batch in extract_data_in_batches(connection, table_name, batch_size=batch_size):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_ext = 'csv' if format_type == 'csv' else 'json'
            filename = f"extraction_{connection.name}_{table_name}_{timestamp}.{file_ext}"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            # Save file in requested format
            with open(filepath, 'w') as f:
                if format_type == 'csv':
                    csv_data = json_to_csv(batch)
                    f.write(csv_data)
                else:
                    json.dump(batch, f, default=str)

            # Create ExtractedData record
            extracted_data = ExtractedData.objects.create(
                connection=connection,
                data=batch
            )

            # Create StoredFile record linked to ExtractedData
            user = request.user if request.user.is_authenticated else None
            StoredFile.objects.create(
                user=user,
                extracted_data=extracted_data,
                filepath=filepath,
                format_type=format_type
            )
            return Response({
                "data": batch,
                "extracted_data_id": extracted_data.id,
                "format": format_type,
                "batch_size": batch_size
            }, status=status.HTTP_200_OK)
        
        return Response({"message": "Extraction complete, but no data found."}, status=status.HTTP_200_OK)

    except DatabaseConnection.DoesNotExist:
        return Response({"error": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
