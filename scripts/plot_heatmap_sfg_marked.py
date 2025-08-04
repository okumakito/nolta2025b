def calc_max_eigval(df_in):
  n = df_in.shape[1]
  df = df_in.rank(axis=1).T * utils.mad(df_in)
  df /= (n*(n+1)/12)**0.5
  return np.linalg.eigvalsh(df.cov()).max()

def plot_heatmap_sfg_marked(data_df, organ):
  file_name = '../data/sfg/sfg_summary_gene.csv'
  df = pd.read_csv(file_name)
  df = df[df.clust_no==1]
  if organ not in df.organ.values:
    return 0
  df = df[df.organ==organ]
  df = utils.z_score(data_df[organ].loc[df.gene])
  sr = df.groupby(axis=1,level=0,sort=False).apply(calc_max_eigval)
  df = df.groupby(axis=1,level=0,sort=False).\
    apply(lambda x: (x.T - x.mean(axis=1)).T)
  df = df.abs()
  idx = np.argmax(sr)
  n = len(df)

  fs = 15
  fig, ax = plt.subplots(figsize=(4,3))
  sns.heatmap(df, cmap='Blues', ax=ax, yticklabels=False, cbar=False,
              robust=True)
  ax.set_xlabel(None)
  ax.set_ylabel(None)
  ax.set_title(f'{organ} ({n} genes)', fontsize=fs*1.5, pad=10)
  ax.tick_params(length=0)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)

  sr = df.groupby(axis=1,level=0,sort=False).count().iloc[0]
  for i in sr.cumsum()[:-1]:
    ax.axvline(i, lw=1, c='k')

  i  = sr.cumsum().iat[idx]
  i2 = sr.cumsum().iat[idx-1] if idx else 0
  c = plt.cm.tab10(3)
  ax.plot([i,i,i2,i2,i], [0,n,n,0,0], lw=3, c=c)
  if False:
    ax.set_xticks([(i+i2)/2])
    ax.set_xticklabels([sr.index[idx]], rotation=0, c=c, fontsize=fs)
  else:
    ax.set_xticks(sr.cumsum() - sr/2)
    ax.set_xticklabels(sr.index, fontsize=fs)

  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df

if __name__ == '__main__':
  organ = sys.argv[1]
  hoge = plot_heatmap_sfg_marked(data_df, organ)
