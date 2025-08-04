def calc_deg(data_df, organ, fc):
  df = data_df[organ].copy()
  df = df[df.min(axis=1) > 5]
  print('target genes:', len(df))

  # pca filtering
  if True:
    model = PCA(n_components=2, random_state=0)
    #model.fit(utils.z_score(df).T)
    model.fit(df.T)
    out_list = []
    for comp in model.components_:
      sr = pd.Series(comp, index=df.index)
      idx = sr[(sr - sr.mean()).abs() > 2 * sr.std()].index
      out_list.append(idx)
    df = df.loc[np.unique(np.concatenate(out_list))]
    print('pca:', len(df))

  if True:
    dfm = df.groupby(axis=1, level=0).mean()
    sr = dfm.max(axis=1) - dfm.min(axis=1)
    df = dfm[sr>fc]
    print('fc:', len(df))

  df = df.groupby(axis=1,level=0).mean()
  df = utils.posthoc_clustering(df, min_clust_size=100, phi_scale=1)
  print('posthoc clustering:', len(df))
  df.to_csv('tmp.csv', index=None)
  print(df.clust.value_counts())
  for clust, sr in df.groupby('clust').gene:
    sr.to_csv(f'tmp{clust}.csv', index=None, header=None)
  return df

if __name__ == '__main__':
  organ = sys.argv[1]
  fc = float(sys.argv[2])
  res_df = calc_deg(data_df, organ, fc)
