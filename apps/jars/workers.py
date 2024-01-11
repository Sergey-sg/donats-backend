from os import getenv
import requests

url = getenv('API_JAR')
body = getenv('JAR_POST_BODY')


def get_jar_info(monobank_id):
    data = {}
    body['clientId'] = monobank_id
    response = requests.post(url, json=body)

    if response.status_code == 200:
        data = response.json()
    return (data)


print(get_jar_info())
