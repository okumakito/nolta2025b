def calc_max_eigval(df_in):
  n = df_in.shape[1]
  df = df_in.rank(axis=1).T * utils.mad(df_in)
  df /= (n*(n+1)/12)**0.5
  return np.linalg.eigvalsh(df.cov()).max()

def plot_max_eigval2(data_df):
  file_name = '../data/sfg/sfg_summary_gene.csv'
  df = pd.read_csv(file_name)
  df = df[df.clust_no==1]
  out_list = []
  for (organ, clust_no), sr in df.groupby(['organ','clust_no']).gene:
    print(organ, clust_no)
    sub_df = utils.z_score(data_df[organ].loc[sr])
    sr = sub_df.groupby(axis=1,level=0,sort=False).apply(calc_max_eigval)
    sr.name = organ
    out_list.append(sr)
  df = pd.concat(out_list, axis=1).T
  sr = df.apply(np.argmax, axis=1).sort_values()
  sr = sr[sr>0]
  df = df.loc[sr.index]
  df = df.dropna(axis=1)
  df = utils.z_score(df)
  vmax = np.ceil(df.max().max() / 0.5) * 0.5

  fig, ax = plt.subplots(figsize=(7,6))
  sns.heatmap(df, cmap='Blues', ax=ax, yticklabels=1,
                  cbar_kws=dict(label='normalized maximum eigenvalue',
                                orientation='horizontal', pad=0.1,
                                shrink=0.6, aspect=20), vmin=0, vmax=vmax)
  ax.tick_params(length=0, pad=5)
  ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
  ax.set_xlabel(None)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
  cb = ax.collections[0].colorbar
  cb.outline.set_linewidth(1)
  cb.ax.tick_params(length=4, width=1)
  for i, j in enumerate(sr):
    c = plt.cm.tab10(3)
    #ax.text(j+0.5, i+0.5, 'x', ha='center', va='center', c=c,
    #        fontweight='bold')
    ax.plot([j,j+1,j+1,j,j], [i,i,i+1,i+1,i], c=c, lw=4, zorder=10)
  for i in range(df.shape[0]-1):
    ax.axhline(i+1, lw=1, c='k')
  for i in range(df.shape[1]-1):
    ax.axvline(i+1, lw=1, c='k')
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df

if __name__ == '__main__':
  hoge = plot_max_eigval2(data_df)
