import json
import requests
from os import getenv
from time import sleep
from celery import shared_task
from datetime import datetime

from .models import AmountOfJar, Jar


url = getenv('API_JAR')
body = json.loads(getenv('JAR_POST_BODY'))

if not url or not body:
    raise ValueError(
        "API_JAR and JAR_POST_BODY environment variables must be set.")


def get_jar_data(monobank_id):
    try:
        body['clientId'] = monobank_id
        response = requests.post(url, json=body)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data for jar {monobank_id}: {e}")
        return {}


@shared_task()
def get_statistic_for_jar():
    jars = Jar.objects.filter(date_closed=None)
    for jar in jars:
        jar_data = get_jar_data(jar.monobank_id)
        jar.goal = jar_data.get('jarGoal', jar.goal)
        if jar_data.get('jarStatus') != 'ACTIVE':
            jar.date_closed = datetime.now()
        AmountOfJar.objects.create(jar=jar, sum=jar_data.get('jarAmount', 0))
        jar.save()
        sleep(61)
