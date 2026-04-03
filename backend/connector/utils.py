import psycopg2
import mysql.connector
from pymongo import MongoClient
from clickhouse_driver import Client

def get_connection(db_connection):
    if db_connection.db_type == 'postgres':
        return psycopg2.connect(
            host=db_connection.host,
            port=db_connection.port,
            user=db_connection.username,
            password=db_connection.password,
            dbname=db_connection.database
        )
    elif db_connection.db_type == 'mysql':
        return mysql.connector.connect(
            host=db_connection.host,
            port=db_connection.port,
            user=db_connection.username,
            password=db_connection.password,
            database=db_connection.database
        )
    elif db_connection.db_type == 'mongo':
        return MongoClient(
            host=db_connection.host,
            port=db_connection.port,
            username=db_connection.username,
            password=db_connection.password
        )
    elif db_connection.db_type == 'clickhouse':
        return Client(
            host=db_connection.host,
            port=db_connection.port,
            user=db_connection.username,
            password=db_connection.password,
            database=db_connection.database
        )
    else:
        raise Exception('Unsupported database type')

def extract_data(connection, table_name, batch_size=1000):
    db_type = connection.__class__.__module__.split('.')[0]
    cursor = connection.cursor()

    if db_type == 'psycopg2':
        cursor.execute(f"SELECT * FROM {table_name}")
        while True:
            records = cursor.fetchmany(batch_size)
            if not records:
                break
            yield records
    elif db_type == 'mysql':
        cursor.execute(f"SELECT * FROM {table_name}")
        while True:
            records = cursor.fetchmany(batch_size)
            if not records:
                break
            yield records
    elif db_type == 'pymongo':
        db = connection.get_default_database()
        collection = db[table_name]
        for i in range(0, collection.count_documents({}), batch_size):
            yield list(collection.find().skip(i).limit(batch_size))
    elif db_type == 'clickhouse_driver':
        # ClickHouse driver does not support fetchmany, so we'll have to do it manually
        # This is not efficient for large tables
        total_rows = cursor.execute(f"SELECT count() FROM {table_name}")[0][0]
        for offset in range(0, total_rows, batch_size):
            yield cursor.execute(f"SELECT * FROM {table_name} LIMIT {batch_size} OFFSET {offset}")
