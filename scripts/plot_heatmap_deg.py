def plot_heatmap_deg(data_df, organ):
  df = data_df[organ].copy()
  df = df[df.min(axis=1)>5]
  print('low-expression removed:', len(df))

  # pca filtering
  if True:
    model = PCA(n_components=2)
    model.fit(utils.z_score(df).T)
    out_list = []
    for comp in model.components_:
      sr = pd.Series(comp, index=df.index)
      idx = sr[(sr - sr.mean()).abs() > 2 * sr.std()].index
      out_list.append(idx)
    df = df.loc[np.unique(np.concatenate(out_list))]
    print('pca filtering:', len(df))

  # groupby
  df = df.groupby(axis=1,level=0,sort=False).mean()

  # fold change filtering
  if False:
    sr = df.max(axis=1) - df.min(axis=1)
    df = df[sr > 1]
    print('fold change filtering:', len(df))
    if len(df) == 0:
      return None

  # z-score
  df = utils.z_score(df)

  # posthoc clustering
  if True:
    df2 = utils.posthoc_clustering(df, min_clust_size=50)
    df = df[df.index.isin(df2.gene)]
    print('posthoc clustering:', len(df))
    if len(df) == 0:
      return None

  # save to file
  df.index.to_series().to_csv(f'tmp_{organ}.csv', index=None, header=None)

  # re-clustering
  Z = linkage(df, method='average', metric='correlation')
  df = df.iloc[leaves_list(Z)]
  max_val = df.abs().max().max()

  # plot
  fig, ax = plt.subplots(figsize=(8,4))
  sns.heatmap(df, cmap='RdBu_r', ax=ax, vmin=-max_val, vmax=max_val,
              cbar_kws=dict(label='z-score'))
  ax.tick_params(length=0)
  ax.set_xlabel(None)
  ax.set_ylabel(f'{len(df)} DEGs')
  ax.set_yticks([])
  ax.set_title(organ, fontsize=16, pad=10)
  fig.tight_layout()
  fig.show()
  fig.savefig(f'tmp_{organ}.png')
  return df

if __name__ == '__main__':
  organ = sys.argv[1]
  if organ == 'all':
    for organ in data_df.columns.get_level_values(0).unique():
      plot_heatmap_deg(data_df, organ)
  else:
    hoge = plot_heatmap_deg(data_df, organ)
