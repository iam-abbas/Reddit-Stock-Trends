from flask import Flask, jsonify
from flask_cors import CORS

import csv

app = Flask(__name__)
cors = CORS(app)


@app.route('/get-basic-data', methods=['GET'])
def get_basic_data() -> str:
    with open('./data/df_best_25.csv', 'r') as csvfile:
        reader = list(csv.reader(csvfile))

    return jsonify(reader)
