from django.db import models
from django.contrib.auth.models import User
from .crypto import encrypt_password, decrypt_password


class DatabaseConnection(models.Model):
    DB_TYPE_CHOICES = [
        ('postgresql', 'PostgreSQL'),
        ('mysql', 'MySQL'),
        ('mongodb', 'MongoDB'),
        ('clickhouse', 'ClickHouse'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='database_connections')
    name = models.CharField(max_length=255)
    db_type = models.CharField(max_length=50, choices=DB_TYPE_CHOICES)
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # In a real app, use encrypted fields
    database_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.password = encrypt_password(self.password)
        super().save(*args, **kwargs)

    @property
    def decrypted_password(self):
        return decrypt_password(self.password)

    def __str__(self):
        return self.name


class StoredFile(models.Model):
    FORMAT_CHOICES = [
        ('json', 'JSON'),
        ('csv', 'CSV'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    extracted_data = models.OneToOneField('ExtractedData', on_delete=models.CASCADE, null=True, blank=True, related_name='stored_file')
    filepath = models.CharField(max_length=255)
    format_type = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='json')
    shared_with = models.ManyToManyField(User, related_name='shared_files')
    
    # New fields for better file naming and filtering
    base_filename = models.CharField(max_length=255, null=True, blank=True, help_text="Base filename without timestamp")
    table_name = models.CharField(max_length=255, null=True, blank=True, help_text="Original table name")
    connection_name = models.CharField(max_length=255, null=True, blank=True, help_text="Database connection name")
    extracted_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filepath


class ExtractedData(models.Model):
    connection = models.ForeignKey(DatabaseConnection, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Data from {self.connection.name} at {self.created_at}"
    
    class Meta:
        verbose_name = "Extracted Data"
        verbose_name_plural = "Extracted Data"


class User(models.Model):
    ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='user')

