from django.db import models
from django.contrib.auth.models import User


class DatabaseConnection(models.Model):
    DB_TYPES = [
        ('postgres', 'PostgreSQL'),
        ('mysql', 'MySQL'),
        ('mongo', 'MongoDB'),
        ('clickhouse', 'ClickHouse'),
    ]

    name = models.CharField(max_length=255)
    db_type = models.CharField(max_length=20, choices=DB_TYPES)
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    database = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class StoredFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filepath = models.CharField(max_length=255)
    shared_with = models.ManyToManyField(User, related_name='shared_files')

    def __str__(self):
        return self.filepath

