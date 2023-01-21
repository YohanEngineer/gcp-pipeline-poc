import random
import datetime
import json


def send_data(request):
    if request.method == 'OPTIONS':
        # Allows GET & POST requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    mock = read_json_file('mock.json')
    documents = generate(mock)
    return (documents, 200, headers)


def read_json_file(path):
    with open(path, 'r') as f:
        return json.load(f)


def generate_json_document(min_temp, max_temp, min_hum, max_hum,
                           min_son, max_son, min_poll, max_poll):
    return {
        "adresse": '',
        "humidite": round(random.uniform(min_hum, max_hum), 2),
        "temperature": round(random.uniform(min_temp, max_temp), 0),
        "niveau_sonore": round(random.uniform(min_son, max_son), 2),
        "pollution_air": round(random.uniform(min_poll, max_poll), 2),
        "timestamp": ''
    }


def generate(dictionnary):
    documents = []
    current_date = datetime.datetime.now().isoformat()
    current_hour = current_date.split('T')[1].split(':')[0]
    min_temp = dictionnary[current_hour]['temperature']['min']
    max_temp = dictionnary[current_hour]['temperature']['max']
    min_hum = dictionnary[current_hour]['humidity']['min']
    max_hum = dictionnary[current_hour]['humidity']['max']
    min_son = dictionnary[current_hour]['noise_level']['min']
    max_son = dictionnary[current_hour]['noise_level']['max']
    min_poll = dictionnary[current_hour]['air_pollution']['min']
    max_poll = dictionnary[current_hour]['air_pollution']['max']
    for i in range(1, 101):
        doc = generate_json_document(min_temp, max_temp, min_hum, max_hum,
                                     min_son, max_son, min_poll, max_poll)
        doc['timestamp'] = current_date
        doc['adresse'] = "{} Rue Calmette".format(i)
        documents.append(doc)

    records = {
        "records": documents
    }
    return records
