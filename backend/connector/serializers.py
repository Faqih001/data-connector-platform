from rest_framework import serializers
from .models import DatabaseConnection, StoredFile, ExtractedData
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']


class DatabaseConnectionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = DatabaseConnection
        fields = ['id', 'user', 'name', 'db_type', 'host', 'port', 'username', 'password', 'database_name', 'created_at']
        read_only_fields = ['user', 'created_at']


class StoredFileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    shared_with = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = StoredFile
        fields = ['id', 'user', 'extracted_data', 'filepath', 'format_type', 'shared_with', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'user']


class ExtractedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedData
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
