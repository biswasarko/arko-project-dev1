import pandas as pd

from re import split
def prepare_data(df):
  df['DATE'] = pd.to_datetime(df['DATE'], format="%d-%b-%Y")
  # df_cl_dt['DATE'] = pd.to_datetime(df_cl_dt['CLOSING_DATES'], format="%d-%b-%Y")
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

  display(df)
  for cols in df.columns:
    if cols == 'DATE':
      continue
    else:
      split_cols = cols.split('_')

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

  return df_int