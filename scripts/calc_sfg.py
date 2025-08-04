# mean shift
def calc_sfg(data_df, organ):
  df = data_df[organ].copy()
  print(df.shape)
  df = df[df.min(axis=1)>5]
  print(df.shape)

  df_shift = df - df.groupby(axis=1,level=0).mean()
  sfg_arr = utils.calculate_sfg(df_shift, phi_scale=3)
  print(sfg_arr.size)
  df = utils.posthoc_clustering(df.loc[sfg_arr],
                                min_clust_size=50, phi_scale=1)
  df.to_csv('tmp.csv', index=None)
  print(df.clust.value_counts())
  for clust, sr in df.groupby('clust').gene:
    sr.to_csv(f'tmp{clust}.csv', index=None, header=None)
  return df

if __name__ == '__main__':
  organ = sys.argv[1]
  res_df = calc_sfg(data_df, organ)
