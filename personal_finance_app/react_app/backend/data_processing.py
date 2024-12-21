import pandas as pd
import os


def save_uploaded_file(file, upload_folder):
    file_path = os.path.join(upload_folder, file.filename)
    os.makedirs(upload_folder, exist_ok=True)
    file.save(file_path)
    return file_path


def load_excel(file_path):
    return pd.read_excel(file_path)


def filter_month_end_rows(df):
    if 'Date' not in df.columns:
        raise ValueError("The DataFrame must have a 'Date' column.")
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df[df['Date'].dt.is_month_end]


def append_new_row(df, new_row_data):
    new_row = {header: new_row_data.get(header) for header in df.columns}
    return df.append(new_row, ignore_index=True)


def save_dataframe_to_excel(df, file_path):
    df.to_excel(file_path, index=False)
