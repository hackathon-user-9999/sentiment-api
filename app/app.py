# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello():
# 	return "Hello World!"

# if __name__ == '__main__':
# 	app.run(host='0.0.0.0', port=8000)


# import os
# import json
# import requests

# PROJECT_ID = ''
# MODEL = 'claude-3-opus@20240229'
# LOCATION = 'us-east5'

# access_token = os.popen('gcloud auth print-access-token').read().strip()

# request_data = {"message": "hello world"}

# url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/anthropic/models/{MODEL}:streamRawPredict"
# headers = {
#     'Authorization': f'Bearer {access_token}',
#     'Content-Type': 'application/json; charset=utf-8'
# }

# try:
#     response = requests.post(url, headers=headers, json=request_data)
#     print(response)
# except requests.exceptions.RequestException as e:
#     print(f'Error: {e}')

# #1---------------

PROJECT_ID = "formula-e24lon-166"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type: "string"}

import vertexai

vertexai.init(project=PROJECT_ID, location=LOCATION)

import pandas as pd
import google.generativeai as genai
from google.cloud import storage
from vertexai.preview.language_models import (ChatModel, InputOutputTextPair,
                                              TextEmbeddingModel,
                                              TextGenerationModel)

genai.configure(api_key='AIzaSyAJscD_SL9ioaVmP_vGrhYXVusMRT2dQYo')
model = genai.GenerativeModel('gemini-1.5-flash')
bucket_name = "formulae-166-cs-bucket"

client = storage.Client()

bucket = storage.Bucket(client, bucket_name)
all_blobs = list(client.list_blobs(bucket_name))

summary_prompt_template = "Provide a summary of the following transcript: "
sentiment_prompt_template = "Provide the sentiment of the below transcript. Example 1: The food wasn't good. Sentiment: Negative. Example 2: This driving is dangerous. Sentiment: Negative. "
actionable_feedback_prompt_template = """Provide a few actions that can be taken /
                                        as a result of the following feedback. Where applicable,/
                                        provide a category alongside these action points, such as /
                                        security, catering, ticketing, safety, etc. Where applicable, /
                                        Provide the sentiment of the action point. Example 1: The /
                                        food was good. Sentiment: Positive. Example 2: /
                                        This driving is dangerous. Sentiment: Negative. /
                                        Example 3: The attendance was fine. Sentiment: Neutral.
                                        Example 4: The was not enough shade. Sentiment: Negative. /
                                        Return this response in JSON format. """

for blob in all_blobs:
    if "txt" in blob.name:
        text_blob = blob.download_as_bytes().decode()
        prompt = actionable_feedback_prompt_template+text_blob
        response = model.generate_content(prompt)
        print(f"Input: {text_blob}, Actions: {response.text}")
