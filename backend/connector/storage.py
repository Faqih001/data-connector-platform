import os
import json
from datetime import datetime

def store_data(data, source_metadata):
    # Store in DB
    # This is a placeholder. You would typically have a model and save each item.
    print("Storing in DB:", data)

    # Store as file
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"data_{timestamp}.json"
    filepath = os.path.join("data", filename)
    os.makedirs("data", exist_ok=True)

    file_content = {
        "timestamp": timestamp,
        "source_metadata": source_metadata,
        "data": data
    }

    with open(filepath, 'w') as f:
        json.dump(file_content, f, indent=4)
    
    return filepath
