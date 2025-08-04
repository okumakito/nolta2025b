def calc_drop_list(count_df):
  df = count_df.copy()
  df.columns = [df.columns.str.split('_').str[0], df.columns]
  organ_idx = df.columns.get_level_values(0).unique()
  idx = df.index
  rp_idx = idx[(idx.str.startswith('Rpl') | idx.str.startswith('Rps'))
               & ~idx.str.startswith('Rps6k')]

  out_list = []
  for organ in organ_idx:
    print(organ)
    sub_df = df[organ]
    while True:
      sr = sub_df.loc[rp_idx].mean() / sub_df.drop(rp_idx, axis=0).median()
      mad = (sr - sr.median()).abs().median()
      idx = sr[sr - sr.median() > 3 * mad].index
      print(idx)
      if len(idx) == 0:
        break
      out_list.append(idx)
      sub_df = sub_df.drop(idx, axis=1)

  # manual
  add_list = ['ewat_3w_2','olf_4w_6','pit_1w_2']
  out_list.append(add_list)
      
  sr_out = pd.Series(np.concatenate(out_list)).sort_values()
  df_out = sr_out.str.split('_', expand=True)
  df_out.columns = ['organ', 'time', 'no']
  df_out.to_csv('tmp.csv', index=False)
  return df_out
    
if __name__ == '__main__':
  if 'count_df' not in locals():
    count_df = load_data_count()
  hoge = calc_drop_list(count_df)
