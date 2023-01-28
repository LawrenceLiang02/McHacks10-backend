from flask_cors import CORS
import requests
from flask import Flask, request, jsonify, make_response
from decouple import config
import io
import os
from google.cloud import vision

app = Flask(__name__)

# Imports the Google Cloud client library
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'cred.json'

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/search', methods=['GET', 'POST'])
def select_all_from_db():
    query = ReadLabel()
    labels = []
    for label in query:
        labels.append(SearchCalorieNinja(label.description))
    # query = request.json["query"]
    # data = SearchCalorieNinja(query)
    return jsonify(labels)


def SearchCalorieNinja(query):
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    response = requests.get(api_url + query, headers={'X-Api-Key': config('CalorieNinja')})
    if response.status_code == requests.codes.ok:
        return(response.text)
    else:
        print("Error:", response.status_code, response.text)


def ReadLabel():
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath('.\Images\Spaghetti-with-Meat-Sauce-Recipe-1-1200.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)

    return labels

