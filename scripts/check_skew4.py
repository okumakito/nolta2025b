def check_skew4(data_df, organ, count_df):
  df = data_df[organ].copy()
  df = df[df.mean(axis=1)>5]
  df = df[df.min(axis=1)>0]
  sr = df.skew(axis=1).sort_values()
  df = count_df.T[count_df.columns.str.startswith(organ)].T
  df = df.loc[sr.index[:10]]
  df.T.to_csv('tmp.csv')
  return df

if __name__ == '__main__':
  if 'count_df' not in locals():
    count_df = load_data_count()
  organ = sys.argv[1]
  hoge = check_skew4(data_df, organ, count_df)
