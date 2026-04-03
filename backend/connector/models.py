from django.db import models

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

