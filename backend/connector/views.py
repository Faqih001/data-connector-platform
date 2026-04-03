from rest_framework import viewsets
from .models import DatabaseConnection
from .serializers import DatabaseConnectionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_connection, extract_data
from rest_framework.decorators import api_view

class DatabaseConnectionViewSet(viewsets.ModelViewSet):
    queryset = DatabaseConnection.objects.all()
    serializer_class = DatabaseConnectionSerializer

class ExtractDataView(APIView):
    def post(self, request, *args, **kwargs):
        connection_id = request.data.get('connection_id')
        table_name = request.data.get('table_name')
        batch_size = request.data.get('batch_size', 1000)

        try:
            db_connection = DatabaseConnection.objects.get(id=connection_id)
            connection = get_connection(db_connection)
            data_generator = extract_data(connection, table_name, batch_size)

            # For simplicity, we'll just return the first batch
            first_batch = next(data_generator)
            return Response(first_batch)

        except DatabaseConnection.DoesNotExist:
            return Response({'error': 'Database connection not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

from .storage import store_data

@api_view(['POST'])
def submit_data(request):
    data = request.data.get('data')
    source_metadata = request.data.get('source_metadata')
    
    # Basic validation
    if not data or not isinstance(data, list):
        return Response({'error': 'Invalid data format'}, status=400)

    filepath = store_data(data, source_metadata)
    
    return Response({'status': 'success', 'filepath': filepath})

