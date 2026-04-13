from .connectors import get_connector
import csv
import io
import json

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

def json_to_csv(json_data):
    """Convert JSON data (list of dicts) to CSV format string"""
    if not json_data:
        return ""
    
    output = io.StringIO()
    fieldnames = list(json_data[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in json_data:
        # Ensure all values are properly serialized
        serialized_row = {
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) if v is not None else ""
            for k, v in row.items()
        }
        writer.writerow(serialized_row)
    
    return output.getvalue()
