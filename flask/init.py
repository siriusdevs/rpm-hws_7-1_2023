import requests
from json import load

with open('input_data.json') as file_to_read:
    start_data = load(file_to_read)


for body in start_data:
    url = 'http://localhost:5000/index/create'
    headers = {'Content-Type': 'application/json', 'Authorization': 'MAX2288'}
    requests.post(url, json=body, headers=headers)
