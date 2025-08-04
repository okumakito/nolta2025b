# each time point
def calc_sfg2(data_df, organ):
  df = data_df[organ].copy()

  out_list = []
  for time, sub_df in df.groupby(axis=1, level=0, sort=False):
     df2 = sub_df[sub_df.min(axis=1) > 5]
     sfg_arr = utils.calculate_sfg(df2)
     print(time, sfg_arr.size)
     out_list.append(sfg_arr)
  sfg_arr = np.unique(np.concatenate(out_list))
  df = utils.posthoc_clustering(df.loc[sfg_arr],
                                min_clust_size=50)
  df.to_csv('tmp.csv', index=None)
  print(df.clust.value_counts())
  for clust, sr in df.groupby('clust').gene:
    sr.to_csv(f'tmp{clust}.csv', index=None, header=None)
  return df

if __name__ == '__main__':
  organ = sys.argv[1]
  res_df = calc_sfg2(data_df, organ)
