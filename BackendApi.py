from flask_cors import CORS
import requests
from flask import Flask, request, jsonify, make_response
from decouple import config

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/search', methods=['GET', 'POST'])
def select_all_from_db():
    query = request.json["query"]
    data = SearchCalorieNinja(query)
    return jsonify(data)


def SearchCalorieNinja(query):
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    response = requests.get(api_url + query, headers={'X-Api-Key': config('CalorieNinja')})
    if response.status_code == requests.codes.ok:
        return(response.text)
    else:
        print("Error:", response.status_code, response.text)


