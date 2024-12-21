from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from data_processing import (
    save_uploaded_file,
    load_excel,
    filter_month_end_rows,
    append_new_row,
    save_dataframe_to_excel,
)
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

global_df = None
file_path = None


@app.route('/upload', methods=['POST'])
def upload_file():
    global global_df, file_path
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    try:
        file_path = save_uploaded_file(file, UPLOAD_FOLDER)
        global_df = load_excel(file_path)
        return jsonify({'message': 'File uploaded successfully', 'columns': list(global_df.columns)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/add-row', methods=['POST'])
def add_row():
    global global_df, file_path
    try:
        row_data = request.json
        global_df = append_new_row(global_df, row_data)
        save_dataframe_to_excel(global_df, file_path)
        return jsonify({'message': 'Row added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/month-end', methods=['GET'])
def get_month_end():
    global global_df
    try:
        month_end_df = filter_month_end_rows(global_df)
        return jsonify({'rows': month_end_df.to_dict(orient='records')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download', methods=['GET'])
def download_file():
    global file_path
    if not file_path:
        return jsonify({'error': 'No file to download'}), 400
    return send_file(file_path, as_attachment=True, download_name='processed_file.xlsx')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
