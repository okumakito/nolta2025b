def check_heatmap_organ(data_df, organ):
  df = data_df[organ].copy()
  #df = df[df.mean(axis=1) > 5]
  df = df[df.min(axis=1) > 0]
  print(df.shape)
  df = df.subtract(df.groupby(axis=1,level=0).mean(),axis=0)
  df = utils.z_score(df)

  fig, axes = plt.subplots(figsize=(8,8), nrows=2)

  ax = axes[0]
  vmax = 5
  sns.heatmap(df, cmap='RdBu_r', yticklabels=False, ax=ax,
              vmax=vmax, vmin=-vmax)
  ax.set_xlabel(None)
  ax.set_ylabel(None)
  ax.tick_params(length=0)

  ax = axes[1]
  sr = df.abs().mean()
  #sr = (df.abs()>5).mean()
  #th = 1   # StringTie
  th = 1.4  # featureCounts
  #th = sr.median() + 10 * (sr - sr.median()).abs().median()
  ax.plot(sr.values)
  ax.axhline(th, c=plt.cm.tab10(3))
  ax.tick_params(length=5)

  sr = sr.groupby(level=0,sort=False).apply(lambda x:x.reset_index(drop=True))
  sr.index = [sr.index.get_level_values(0), sr.index.get_level_values(1)+1]
  print(sr[sr > th])

  fig.tight_layout()
  fig.show()
  return df

if __name__ == '__main__':
  organ = sys.argv[1]
  hoge = check_heatmap_organ(data_df, organ)
