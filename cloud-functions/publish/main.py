import requests
import json
from google.cloud import pubsub_v1
from concurrent import futures
from typing import Callable


def publish_message(data):

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("episen-data-pipeline-poc", "captors")
    publish_futures = []

    def get_callback(
        publish_future: pubsub_v1.publisher.futures.Future, data: str
    ) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
        def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
            try:
                print(publish_future.result(timeout=60))
            except futures.TimeoutError:
                print(f"Publishing {data} timed out.")

        return callback

    # When you publish a message, the client returns a future.
    publish_future = publisher.publish(topic_path, data.encode('utf-8'))
    # Non-blocking. Publish failures are handled in the callback function.
    publish_future.add_done_callback(get_callback(publish_future, data))
    publish_futures.append(publish_future)

    # Wait for all the publish futures to resolve before exiting.
    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

    print(f"Published messages with error handler to {topic_path}.")


def publish(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    data = requests.get(
        'https://europe-west1-episen-data-pipeline-poc.cloudfunctions.net/mock-captor').json()

    records = data['records']

    json_data = json.dumps(records)

    publish_message(json_data)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    return ('OK', 200, headers)
