from rest_framework import serializers
from .models import DatabaseConnection, StoredFile, ExtractedData

class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = '__all__'

class StoredFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoredFile
        fields = '__all__'

class ExtractedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedData
        fields = '__all__'
