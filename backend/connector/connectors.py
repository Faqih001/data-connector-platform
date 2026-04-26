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
import os

# System tables to exclude from user-facing table lists
SYSTEM_TABLE_PREFIXES = (
    'auth_',
    'django_',
    'connector_',
    'sqlite_',
)

def is_system_table(table_name):
    """Check if a table is a system/internal table that should be hidden."""
    return any(table_name.lower().startswith(prefix) for prefix in SYSTEM_TABLE_PREFIXES)

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

def translate_docker_host(host, db_type, port):
    """
    Translate localhost to Docker service names when running in containers.
    Maps localhost ports to Docker service names.
    """
    # If not localhost, return as-is
    if host not in ('localhost', '127.0.0.1', '::1'):
        return host
    
    # Check if running in Docker by looking for Docker environment indicator
    is_docker = os.path.exists('/.dockerenv') or os.getenv('DOCKER_ENV')
    
    if not is_docker:
        return host
    
    # Map database types to Docker service names
    docker_hosts = {
        'postgresql': 'db',
        'mysql': 'mysql',
        'mongodb': 'mongo',
        'clickhouse': 'clickhouse',
    }
    
    # Return Docker service name or original host
    return docker_hosts.get(db_type, host)

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

    def get_columns(self, table_name):
        return []

    def close(self):
        if self.connection:
            self.connection.close()

class PostgresConnector(BaseConnector):
    def connect(self):
        # Use decrypted_password property if available (from Django model)
        password = getattr(self.connection_details, 'decrypted_password', self.connection_details.password)
        # Translate localhost to Docker service name if needed
        host = translate_docker_host(self.connection_details.host, 'postgresql', self.connection_details.port)
        self.connection = psycopg2.connect(
            host=host,
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

    def get_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"
        )
        tables = [row[0] for row in cursor.fetchall()]
        # Filter out system tables
        return [t for t in tables if not is_system_table(t)]

    def get_columns(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position
            """,
            [table_name],
        )
        return [row[0] for row in cursor.fetchall()]

class MySQLConnector(BaseConnector):
    def connect(self):
        # Use decrypted_password property if available (from Django model)
        password = getattr(self.connection_details, 'decrypted_password', self.connection_details.password)
        # Translate localhost to Docker service name if needed
        host = translate_docker_host(self.connection_details.host, 'mysql', self.connection_details.port)
        self.connection = mysql.connector.connect(
            host=host,
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

    def get_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = database() ORDER BY table_name")
        tables = [row[0] for row in cursor.fetchall()]
        # Filter out system tables
        return [t for t in tables if not is_system_table(t)]

    def get_columns(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = database() AND table_name = %s
            ORDER BY ordinal_position
            """,
            [table_name],
        )
        return [row[0] for row in cursor.fetchall()]

class MongoConnector(BaseConnector):
    def connect(self):
        # Use decrypted_password property if available (from Django model)
        password = getattr(self.connection_details, 'decrypted_password', self.connection_details.password)
        # Translate localhost to Docker service name if needed
        host = translate_docker_host(self.connection_details.host, 'mongodb', self.connection_details.port)
        self.connection = pymongo.MongoClient(
            host=host,
            port=self.connection_details.port,
            username=self.connection_details.username,
            password=password,
        )

    def fetch_batch(self, collection_name, batch_size, offset):
        db = self.connection[self.connection_details.database_name]
        collection = db[collection_name]
        rows = list(collection.find().skip(offset).limit(batch_size))
        return [{col: serialize_value(val) for col, val in row.items()} for row in rows]

    def get_tables(self):
        db = self.connection[self.connection_details.database_name]
        collections = db.list_collection_names()
        # Filter out system tables
        return [c for c in collections if not is_system_table(c)]

    def get_columns(self, collection_name):
        db = self.connection[self.connection_details.database_name]
        document = db[collection_name].find_one()
        if not document:
            return []
        return list(document.keys())

class ClickHouseConnector(BaseConnector):
    def connect(self):
        # Use decrypted_password property if available (from Django model)
        password = getattr(self.connection_details, 'decrypted_password', self.connection_details.password)
        # Translate localhost to Docker service name if needed
        host = translate_docker_host(self.connection_details.host, 'clickhouse', self.connection_details.port)
        
        # ClickHouse client connection kwargs
        connect_kwargs = {
            'host': host,
            'port': self.connection_details.port,
            'user': self.connection_details.username,
            'database': self.connection_details.database_name,
        }
        
        # Only add password if it's not empty
        if password:
            connect_kwargs['password'] = password
        
        self.connection = Client(**connect_kwargs)

    def close(self):
        # ClickHouse Client doesn't have a close() method, but we keep this for consistency
        pass

    def fetch_batch(self, table_name, batch_size, offset):
        return self.connection.execute(f"SELECT * FROM {table_name} LIMIT {batch_size} OFFSET {offset}", with_column_types=True)

    def get_tables(self):
        result = self.connection.execute(f"SELECT name FROM system.tables WHERE database = '{self.connection_details.database_name}' ORDER BY name")
        tables = [row[0] for row in result]
        # Filter out system tables
        return [t for t in tables if not is_system_table(t)]

    def get_columns(self, table_name):
        result = self.connection.execute(
            f"SELECT name FROM system.columns WHERE database = '{self.connection_details.database_name}' AND table = '{table_name}' ORDER BY position"
        )
        return [row[0] for row in result]

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
