from flask import jsonify

import config
import pandas as pd

def expenseDashboard():
    expense_df = pd.read_csv(config.expense_data_path)
    exp_df = process_exp_df(expense_df)
    # print(exp_df.to_json(orient="records"))

    return 200


def convert_to_json(df):
    dates = []
    expense = []
    for index, row in df.iterrows():
        dates.append(row['Date'])
        expense.append(row['Expense'])
        # row_data = {
        #     row['Date'] : {
        #         'Category' : row['Category'],
        #         'Expense' : row['Expense']
        #     }
        # }
        # json_data.update(row_data)
    print(df)
    print(dates)
    print(expense)

def process_exp_df(expense_df, date_start='2024-12-01', date_end='2024-12-31', cat=['FnB'], subcat=['All'],  item=None):
    if len(cat) > 1:
        subcat = ['All']

    expense_df = expense_df[(expense_df['Date'] >= date_start) & (expense_df['Date'] <= date_end)]
    if cat[0] == 'All':
        exp_df = expense_df.groupby(['Date']).sum('Expense').reset_index()
    else:
        exp_df = expense_df[expense_df['Category'].isin(cat)]
        exp_df = exp_df.groupby(['Date', 'Category']).sum('Expense').reset_index()
        if subcat[0] != 'All':
            exp_df = expense_df[expense_df['SubCategory'].isin(subcat)]
            exp_df = exp_df.groupby(['Date', 'Category', 'SubCategory']).sum('Expense').reset_index()
    # else
    # expense_df = expense_df.groupby(['Date', 'Category', 'SubCategory']).sum('Expense').reset_index()
    # exp_df = expense_df.groupby(['Date', 'Category', 'SubCategory']).sum('Expense').reset_index()
    # exp_df_dt =
    exp_json = convert_to_json(exp_df)
    return exp_df

expenseDashboard()