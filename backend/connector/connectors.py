import psycopg2
import mysql.connector
import pymongo
from bson import ObjectId
from clickhouse_driver import Client
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from decimal import Decimal
import json

def serialize_value(obj):
    """Convert non-JSON-serializable objects to serializable formats."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, ObjectId):
        return str(obj)
    elif obj is None:
        return None
    else:
        return obj

class BaseConnector(ABC):
    def __init__(self, connection_details):
        self.connection_details = connection_details
        self.connection = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def fetch_batch(self, table_name, batch_size, offset):
        pass

    def close(self):
        if self.connection:
            self.connection.close()

class PostgresConnector(BaseConnector):
    def connect(self):
        # Use decrypted_password property if available (from Django model)
        password = getattr(self.connection_details, 'decrypted_password', self.connection_details.password)
        self.connection = psycopg2.connect(
            host=self.connection_details.host,
            port=self.connection_details.port,
            user=self.connection_details.username,
            password=password,
            dbname=self.connection_details.database_name,
        )

    def fetch_batch(self, table_name, batch_size, offset):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {batch_size} OFFSET {offset}")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [{col: serialize_value(val) for col, val in zip(columns, row)} for row in rows]

class MySQLConnector(BaseConnector):
    def connect(self):
        # Use decrypted_password property if available (from Django model)
        password = getattr(self.connection_details, 'decrypted_password', self.connection_details.password)
        self.connection = mysql.connector.connect(
            host=self.connection_details.host,
            port=self.connection_details.port,
            user=self.connection_details.username,
            password=password,
            database=self.connection_details.database_name,
        )

    def fetch_batch(self, table_name, batch_size, offset):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        return [{col: serialize_value(val) for col, val in row.items()} for row in rows]

class MongoConnector(BaseConnector):
    def connect(self):
        # Use decrypted_password property if available (from Django model)
        password = getattr(self.connection_details, 'decrypted_password', self.connection_details.password)
        self.connection = pymongo.MongoClient(
            host=self.connection_details.host,
            port=self.connection_details.port,
            username=self.connection_details.username,
            password=password,
        )

    def fetch_batch(self, collection_name, batch_size, offset):
        db = self.connection[self.connection_details.database_name]
        collection = db[collection_name]
        rows = list(collection.find().skip(offset).limit(batch_size))
        return [{col: serialize_value(val) for col, val in row.items()} for row in rows]

class ClickHouseConnector(BaseConnector):
    def connect(self):
        # Use decrypted_password property if available (from Django model)
        password = getattr(self.connection_details, 'decrypted_password', self.connection_details.password)
        self.connection = Client(
            host=self.connection_details.host,
            port=self.connection_details.port,
            user=self.connection_details.username,
            password=password,
            database=self.connection_details.database_name,
        )

    def fetch_batch(self, table_name, batch_size, offset):
        return self.connection.execute(f"SELECT * FROM {table_name} LIMIT {batch_size} OFFSET {offset}", with_column_types=True)

def get_connector(connection_details):
    if connection_details.db_type == 'postgresql':
        return PostgresConnector(connection_details)
    elif connection_details.db_type == 'mysql':
        return MySQLConnector(connection_details)
    elif connection_details.db_type == 'mongodb':
        return MongoConnector(connection_details)
    elif connection_details.db_type == 'clickhouse':
        return ClickHouseConnector(connection_details)
    else:
        raise ValueError("Unsupported database type")
