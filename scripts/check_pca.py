def check_pca(data_df, organ, pc):
  df = data_df[organ].copy()
  df = df[df.min(axis=1) > 5]
  df = utils.z_score(df)
  model = PCA(n_components=pc)
  model.fit(df.T)
  sr = pd.Series(model.components_[-1], index=df.index.values)
  sr = sr.sort_values(ascending=False)
  df = df.loc[sr.index]
  vmax = df.quantile(0.99).max()

  fig, axes = plt.subplots(figsize=(8,8), nrows=2)

  ax = axes[0]
  sns.heatmap(df, cmap='RdBu_r', ax=ax, vmax=vmax, vmin=-vmax)
  ax.set_title(f'{organ} PC{pc}', fontsize=16, pad=10)  
  n_sr = df.groupby(axis=1,level=0,sort=False).count().iloc[0]
  ax.set_xticks(n_sr.cumsum() - n_sr/2)
  ax.set_xticklabels(n_sr.index)
  for i in n_sr.cumsum()[:-1]:
    ax.axvline(i, lw=1, c='k')

  ax = axes[1]
  sns.heatmap(df.groupby(axis=1,level=0,sort=False).mean(), cmap='RdBu_r',
              ax=ax, vmax=vmax, vmin=-vmax)

  for ax in axes:
    ax.set_xlabel(None)
    ax.set_ylabel('genes')
    ax.set_yticks([])
    ax.tick_params(length=0)

  fig.tight_layout()
  fig.show()
  return df

if __name__ == '__main__':
  organ = sys.argv[1]
  pc = int(sys.argv[2]) # starts from 1
  hoge = check_pca(data_df, organ, pc)
