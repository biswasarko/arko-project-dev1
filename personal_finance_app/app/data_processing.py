import pandas as pd
import matplotlib.pyplot as plt

def prepare_data(df, df_cl_dt):
  df['DATE'] = pd.to_datetime(df['DATE'], format="%d-%b-%Y")
  print(df_cl_dt)
  df_cl_dt['DATE'] = pd.to_datetime(df_cl_dt['Date'], format="%d-%b-%Y")
  df_int = df
  df_int['TOTAL_LQ'] = 0
  df_int['TOTAL_DP'] = 0
  df_int['TOTAL_LB'] = 0
  df_int['TOTAL_MI'] = 0
  df_int['TOTAL_MV'] = 0
  df_int['TOTAL_ARKO'] = 0
  df_int['TOTAL_MOMO'] = 0
  df_int['TOTAL_JOINT'] = 0
  df_int['TOTAL_MI_EQ'] = 0
  df_int['TOTAL_MI_MF'] = 0
  df_int['TOTAL_MV_EQ'] = 0
  df_int['TOTAL_MV_MF'] = 0

  for cols in df.columns:
    if cols == 'DATE':
      continue
    else:
      split_cols = cols.split('_')
      df_int[cols] = df_int[cols].astype('int')

    if split_cols[0] == 'TOTAL':
      continue

    col_sfx_cat = split_cols[0]
    col_sfx_subcat = split_cols[1]
    col_sfx_brand = split_cols[2]
    col_sfx_user = split_cols[3]

    if col_sfx_cat == 'LQ':
      df_int['TOTAL_LQ'] = df_int['TOTAL_LQ'] + df[cols]
    elif col_sfx_cat == 'DP':
      df_int['TOTAL_DP'] = df_int['TOTAL_DP'] + df[cols]
    elif col_sfx_cat == 'LB':
      df_int['TOTAL_LB'] = df_int['TOTAL_LB'] + df[cols]
    elif col_sfx_cat == 'MI':
      df_int['TOTAL_MI'] = df_int['TOTAL_MI'] + df[cols]
      if col_sfx_subcat == 'EQ':
        df_int['TOTAL_MI_EQ'] = df_int['TOTAL_MI_EQ'] + df[cols]
      elif col_sfx_subcat == 'MF':
        df_int['TOTAL_MI_MF'] = df_int['TOTAL_MI_MF'] + df[cols]
    elif col_sfx_cat == 'MV':
      df_int['TOTAL_MV'] = df_int['TOTAL_MV'] + df[cols]
      if col_sfx_subcat == 'EQ':
        df_int['TOTAL_MV_EQ'] = df_int['TOTAL_MV_EQ'] + df[cols]
      elif col_sfx_subcat == 'MF':
        df_int['TOTAL_MV_MF'] = df_int['TOTAL_MV_MF'] + df[cols]

    if (col_sfx_user == 'ARKO') & (col_sfx_cat != 'MI'):
      df_int['TOTAL_ARKO'] = df_int['TOTAL_ARKO'] + df[cols]
    elif (col_sfx_user == 'MOMO') & (col_sfx_cat != 'MI'):
      df_int['TOTAL_MOMO'] = df_int['TOTAL_MOMO'] + df[cols]
    elif (col_sfx_user == 'JOINT') & (col_sfx_cat != 'MI'):
      df_int['TOTAL_JOINT'] = df_int['TOTAL_JOINT'] + df[cols]

  return df_int, df_cl_dt

def create_df_net(df_int):
  # df_net = pd.DataFrame()
  df_net = df_int
  # df_net['DATE'] = df_int['DATE']
  df_net['GROSS_TOTAL'] = df_int['TOTAL_LQ'] + df_int['TOTAL_DP'] + df_int['TOTAL_MV']
  df_net['NET_TOTAL'] = df_net['GROSS_TOTAL'] - df_int['TOTAL_LB']
  return df_net

def create_df_closing(df_net, df_cl_dt):
  df_closing = df_net[df_net['DATE'].isin(df_cl_dt['DATE'])]
  df_closing['DATE_YY_MM'] = df_closing['DATE'].dt.strftime("%Y-%m")
  df_closing['DIFF_LQ'] = df_closing['TOTAL_LQ'] - df_closing['TOTAL_LQ'].shift(1)
  df_closing['DIFF_DP'] = df_closing['TOTAL_DP'] - df_closing['TOTAL_DP'].shift(1)
  df_closing['DIFF_MV'] = df_closing['TOTAL_MV'] - df_closing['TOTAL_MV'].shift(1)
  df_closing['DIFF_LB'] = df_closing['TOTAL_LB'] - df_closing['TOTAL_LB'].shift(1)
  df_closing['GROSS_DIFF'] = df_closing['GROSS_TOTAL'] - df_closing['GROSS_TOTAL'].shift(1)
  df_closing['NET_DIFF'] = df_closing['NET_TOTAL'] - df_closing['NET_TOTAL'].shift(1)
  df_closing['DIFF_MI'] = df_closing['TOTAL_MI'] - df_closing['TOTAL_MI'].shift(1)
  return df_closing

def generate_reports(df_closing, df_net):
  print(
    df_closing[['DATE_YY_MM', 'TOTAL_LQ', 'TOTAL_MV', 'TOTAL_DP', 'TOTAL_LB', 'GROSS_TOTAL', 'NET_TOTAL']].tail(12))
  print(df_closing[['DATE_YY_MM', 'DIFF_LQ', 'DIFF_MV', 'DIFF_DP', 'DIFF_LB', 'GROSS_DIFF', 'NET_DIFF']].tail(12))
  # display(df_closing[['DATE_YY_MM', 'DIFF_LQ', 'DIFF_MV', 'DIFF_DP', 'DIFF_LB', 'GROSS_DIFF', 'NET_DIFF']].tail(12))

  df_savings = df_closing[['DATE_YY_MM', 'GROSS_DIFF', 'NET_DIFF']]
  print(df_savings.tail(12))

def generate_charts(df_closing):
  # prompt: show grid lines in the previous chart

  fig, ax = plt.subplots(figsize=(20, 12))
  # Create a line chart for gross_total and net_total
  plt.plot(df_closing['DATE'], df_closing['GROSS_TOTAL'], label='Gross Total')
  plt.plot(df_closing['DATE'], df_closing['NET_TOTAL'], label='Net Total')

  # Set the title and axis labels
  plt.title('Gross and Net Totals Over Time')
  plt.xlabel('Date')
  plt.ylabel('Amount')

  # Display the legend
  plt.legend()

  # Add grid lines
  plt.grid(True)

  # Format y-axis labels with commas and millions
  plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f} M'))

  # Rotate x-axis labels for readability
  plt.xticks(rotation=45)

  # Show the plot
  plt.show()

def generate_charts_2(df_net):
  df_weekly_report = df_net[['DATE', 'TOTAL_LQ', 'TOTAL_MV', 'TOTAL_DP', 'TOTAL_LB', 'GROSS_TOTAL', 'NET_TOTAL']].tail(12)
  print(df_weekly_report)
  # Create a figure and axes object.
  fig, ax = plt.subplots(figsize=(20, 12))

  # Plot the data for each column in df_weekly_report.
  ax.plot(df_weekly_report['DATE'], df_weekly_report['NET_TOTAL'], label = 'NET_TOTAL')
  ax.plot(df_weekly_report['DATE'], df_weekly_report['GROSS_TOTAL'], label = 'GROSS_TOTAL')
  ax.plot(df_weekly_report['DATE'], df_weekly_report['TOTAL_MV'], label = 'TOTAL_MV')
  ax.plot(df_weekly_report['DATE'], df_weekly_report['TOTAL_LQ'], label = 'TOTAL_LQ')
  ax.plot(df_weekly_report['DATE'], df_weekly_report['TOTAL_DP'], label = 'TOTAL_DP')
  ax.plot(df_weekly_report['DATE'], df_weekly_report['TOTAL_LB'], label = 'TOTAL_LB')

  # Set the title and axis labels.
  ax.set_title('Weekly Report')
  ax.set_xlabel('Date')
  ax.set_ylabel('Amount')

  # Add a legend and grid.
  ax.legend()
  ax.grid(True)

  # Show the plot.
  plt.show()

def gen_pie_chart(df_weekly_report):

  # Extract data for the last day
  last_day_data = df_weekly_report.iloc[-1, :]

  # Define labels and values for the pie chart
  labels = ['Total MV', 'Total LQ', 'Total DP', 'Total LB']
  values = [last_day_data['TOTAL_MV'], last_day_data['TOTAL_LQ'], last_day_data['TOTAL_DP'], last_day_data['TOTAL_LB']]

  # Create and customize the pie chart
  fig, ax = plt.subplots()
  ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
  ax.set_title("Breakdown of Networth")

  # Display the pie chart
  plt.show()

def display_user(df_net):
  print(df_net[['DATE', 'TOTAL_MOMO', 'TOTAL_ARKO', 'TOTAL_JOINT']].tail(1))

def run_processing(df, df_cl_dt):
  df_int, df_cl_dt = prepare_data(df, df_cl_dt)
  df_net = create_df_net(df_int)
  df_closing = create_df_closing(df_net, df_cl_dt)
  generate_reports(df_closing, df_net)
  generate_charts(df_closing)
  generate_charts_2(df_net)
  df_weekly_report = df_net[['DATE', 'TOTAL_LQ', 'TOTAL_MV', 'TOTAL_DP', 'TOTAL_LB', 'GROSS_TOTAL', 'NET_TOTAL']].tail(12)
  gen_pie_chart(df_weekly_report)
  display_user(df_net)

