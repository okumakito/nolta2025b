def adjust_simple_linear_regression(df_in, sub_idx, organ_list):
  out_list = []
  for organ, sub_df_in in df_in.groupby(axis=1, level=0):
    sub_df = sub_df_in.copy()
    if organ in organ_list:
      sr = sub_df.loc[sub_idx].mean()
      sr = (sr - sr.mean()) / sr.std()
      sub_df[sub_df==0] = None
      shift_df = sub_df.subtract(sub_df.mean(axis=1),axis=0)
      beta_sr = (shift_df * sr).mean(axis=1)
      sub_df -= np.outer(beta_sr, sr)
      sub_df = sub_df.clip(0).fillna(0)
    out_list.append(sub_df)
  df_out = pd.concat(out_list, axis=1)
  return df_out

def format_data_norm():
  data_file = '../data/data_norm.csv'
  drop_file = '../data/drop_list.csv'
  df = pd.read_csv(data_file, index_col=0)

  # parse columns
  col_orig = df.columns
  df2 = df.columns.str.split('_', expand=True).to_frame()
  df.columns = [df2[0], df2[1], df2[2]]
  df.columns.names = ['organ','time', 'replicate']

  # RP adjustment
  idx = df.index
  organ_list = ['bat','ewat','gas','iwat','panc','pit','sol']
  rp_idx = idx[(idx.str.startswith('Rpl') | idx.str.startswith('Rps'))
               & ~idx.str.startswith('Rps6k')]
  df = adjust_simple_linear_regression(df, rp_idx, organ_list)

  # CD adjustment for only iwat
  cd_idx = idx[idx.str.match('Cd\d')]
  organ_list = ['iwat']
  df = adjust_simple_linear_regression(df, cd_idx, organ_list)

  # remove outliers
  if True:
    df_drop = pd.read_csv(drop_file, dtype=str)
    drop_tpl_list = [tuple(x) for _, x in df_drop.iterrows()]
    df = df.drop(drop_tpl_list, axis=1)

  # remove all-zero rows
  df = df[df.sum(axis=1)>0]

  # round
  df = df.round(4)

  # save to file
  df.columns = df.columns.get_level_values(0) + '_' +\
    df.columns.get_level_values(1) + '_' +\
    df.columns.get_level_values(2)
  df.to_csv('tmp.csv')

  return df

if __name__ == '__main__':
  hoge = format_data_norm()
