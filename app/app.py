# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello():
# 	return "Hello World!"

# if __name__ == '__main__':
# 	app.run(host='0.0.0.0', port=8000)


import os
import json
import requests

PROJECT_ID = 'your-gcp-project-id'
MODEL = 'claude-3-opus@20240229'
LOCATION = 'us-east5'

access_token = os.popen('gcloud auth print-access-token').read().strip()

request_data = {"message": "hello world"}

url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/anthropic/models/{MODEL}:streamRawPredict"
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json; charset=utf-8'
}

try:
    response = requests.post(url, headers=headers, json=request_data)
    print(response)
except requests.exceptions.RequestException as e:
    print(f'Error: {e}')
