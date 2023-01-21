import base64
import tempfile
import json
import csv
from datetime import datetime
from google.cloud import storage

storage_client = storage.Client()


def upload_message(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    pubsub_message = pubsub_message.replace("'", '"')
    now = datetime.now()
    records = json.loads(pubsub_message)
    print(records)
    now = datetime.now()
    filename = f'data_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}.csv'
    _, temp_local_filename = tempfile.mkstemp()
    with open(temp_local_filename, 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile, delimiter=';')

        # Iterate over the records and write each one to the CSV file
        for data in records:
            adresse = data['adresse']
            humidite = data['humidite']
            niveau_sonore = data['niveau_sonore']
            pollution_air = data['pollution_air']
            temperature = data['temperature']
            timestamp = data['timestamp']
            writer.writerow([adresse, humidite, niveau_sonore,
                            pollution_air, temperature, timestamp])

    input_bucket = storage_client.bucket('bucket-transit-poc')
    new_blob = input_bucket.blob(filename)
    new_blob.upload_from_filename(temp_local_filename)
    print(f'File {filename} saved into bucket!')
