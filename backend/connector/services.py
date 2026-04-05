from .connectors import get_connector

def extract_data_in_batches(connection_details, table_name, batch_size=1000):
    connector = get_connector(connection_details)
    connector.connect()
    offset = 0
    while True:
        batch = connector.fetch_batch(table_name, batch_size, offset)
        if not batch:
            break
        yield batch
        offset += batch_size
    connector.close()
