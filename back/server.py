import sys
from flask import Flask, jsonify
from flask_cors import CORS

import csv

app = Flask(__name__)
cors = CORS(app)
data_file = sys.argv[1] if len(sys.argv) > 1 else './data/df_best_25.csv'

print('Using data file {}'.format(data_file))


@app.route('/get-basic-data', methods=['GET'])
def get_basic_data() -> str:
    with open(data_file, 'r') as f:
        data = list(csv.reader(f))

    return jsonify(data)
