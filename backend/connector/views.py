from rest_framework import viewsets
from .models import DatabaseConnection
from .serializers import DatabaseConnectionSerializer

class DatabaseConnectionViewSet(viewsets.ModelViewSet):
    queryset = DatabaseConnection.objects.all()
    serializer_class = DatabaseConnectionSerializer

