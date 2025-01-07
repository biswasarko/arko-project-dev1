def process_exp_df(expense_df, filter):
    date_start = filter['Date_Start']
    date_end = filter['Date_End']
    category = filter['Category']
    expense_df = expense_df[(expense_df['Date'] >= date_start) & (expense_df['Date'] <= date_end)]
    if category != 'All':
        expense_df = expense_df[expense_df['Category'] == category]
    expense_df = expense_df.groupby(['Date']).sum('Expense').reset_index()
    print(expense_df)
    tot_df = expense_df['Expense'].sum()
    print(tot_df)
    return expense_df, tot_df