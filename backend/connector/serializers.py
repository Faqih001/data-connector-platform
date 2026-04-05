from rest_framework import serializers
from .models import DatabaseConnection, StoredFile

class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = '__all__'

class StoredFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoredFile
        fields = '__all__'
