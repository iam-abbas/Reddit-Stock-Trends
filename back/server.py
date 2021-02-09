from flask import Flask, jsonify

import pandas as pd

app = Flask(__name__)

@app.route('/get-basic-data', methods=['GET'])
def get_basic_data() -> str:
	best_ticks_data = pd.read_csv('./data/df_best_25.csv')
	return best_ticks_data.to_json()
