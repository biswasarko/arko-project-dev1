import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from datetime import datetime
import config

app = Flask(__name__)
CORS(app)

EXP_FILE_PATH = config.expense_data_path
NET_FILE_PATH = config.networth_data_path

global_df = None
closing_dts_df = None
file_path = None
std_df = None

# Ensure the CSV file exists
if not os.path.exists(EXP_FILE_PATH):
    with open(EXP_FILE_PATH, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Expense", "Item", "Category", "SubCategory", "Payment_Method", "Essential_Flag"])

def preprocess_file():
    global global_df, closing_dts_df
    global_df = pd.read_excel(NET_FILE_PATH, sheet_name='PERFORMANCE')
    closing_dts_df = pd.read_excel(NET_FILE_PATH, sheet_name='CLOSING_DATES')
    headers = global_df.columns.tolist()
    return global_df, closing_dts_df, headers

def create_schema_from_headers(headers):
    schema = {"fields": []}
    for h in headers:
        if 'date' in h.lower():
            field = {"name": h, "label": h.upper(), "type": "date", "required": "true"}
            schema["fields"].append(field)
        else:
            field = {"name": h, "label": h.upper(), "type": "number", "required": "true", "defaultValue": 0}
            schema["fields"].append(field)
    print(schema)
    return schema

@app.route('/get_headers', methods=['GET'])
def get_headers():
    preprocess_file()
    headers = global_df.columns.tolist()
    schema = create_schema_from_headers(headers)
    # print(headers)
    return jsonify(schema), 200

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    print('inside')
    print(data)
    # sub_category = data.get("Sub_Category")
    # data["Category"] = CATEGORY_MAPPING.get(sub_category, "Other")
    with open(EXP_FILE_PATH, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data.get(key) for key in ["Date", "Expense", "Item", "Category", "SubCategory", "Payment_Method", "Essential_Flag"]])
    return jsonify({"status": "success"}), 200

@app.route('/transactions', methods=['GET'])
def transactions():
    with open(EXP_FILE_PATH, 'r') as file:
        rows = list(csv.DictReader(file))
    return jsonify(rows[-10:]), 200

if __name__ == '__main__':
    app.run(debug=True)
