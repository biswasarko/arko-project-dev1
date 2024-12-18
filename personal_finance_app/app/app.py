from flask import Flask, request, render_template, send_file
import pandas as pd
import os
from io import BytesIO
from data_processing import prepare_data

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

global_df = None
file_path = None
std_df = None

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def process_file():
    global global_df, file_path
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    print(file)

    if file.filename == '':
        return "No file selected", 400

    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # load excel into a df
        global_df = pd.read_excel(file_path)
        headers = global_df.columns.tolist()
        return render_template('form.html', headers=headers, rows=global_df.to_dict(orient='records'))

    except Exception as e:
        return f"Error processing file: {str(e)}", 500

@app.route('/process', methods=['POST'])
def process_data():
    global global_df, file_path, std_df
    try:
        # Get the form data for a new row
        new_row = pd.DataFrame.from_dict({header: [request.form.get(header)] for header in global_df.columns})
        print(new_row)
        std_df = pd.concat([global_df, new_row], ignore_index=True)

        # Perform aggregation
        row_count = len(std_df)
        aggregation_result = f"Total rows: {row_count}"

        df_int = prepare_data(std_df)

        # Save updated dataframe back to the file
        # df_net.to_excel(file_path, index=False)

        return render_template('form.html', headers=df_int.columns.tolist(),
                               rows=df_int.to_dict(orient='records'), aggregation_result=aggregation_result)
    except Exception as e:
        return f"Error processing data: {str(e)}", 500

@app.route('/download', methods=['GET'])
def download_file():
    global file_path
    if not file_path:
        return "No file to download", 400
    return send_file(file_path, as_attachment=True, download_name="Networth_demo.xlsx")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)