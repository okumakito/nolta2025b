def load_data():
  data_file = '../data/data_norm_adj.csv'
  drop_file = '../data/drop_list.csv'
  df = pd.read_csv(data_file, index_col=0)

  # parse columns
  df2 = df.columns.str.split('_', expand=True).to_frame()
  df.columns = [df2[0], df2[1], df2[2]]
  df.columns.names = ['organ','time', 'replicate']

  # remove outliers
  if False:
    df_drop = pd.read_csv(drop_file, dtype=str)
    drop_tpl_list = [tuple(x) for _, x in df_drop.iterrows()]
    df = df.drop(drop_tpl_list, axis=1)

  # remove replicate number
  df.columns = df.columns.droplevel(2)

  # sort only organs
  df = df[df.columns.get_level_values(0).unique().sort_values()].copy()

  return df

if __name__ == '__main__':
  data_df = load_data()
