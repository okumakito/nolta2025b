def calc_max_eigval(df_in):
  n = df_in.shape[1]
  df = df_in.rank(axis=1).T * utils.mad(df_in)
  df /= (n*(n+1)/12)**0.5
  return np.linalg.eigvalsh(df.cov()).max()

def plot_max_eigval(data_df):
  file_name = '../data/sfg/sfg_summary_gene.csv'
  df = pd.read_csv(file_name)
  out_list = []
  for (organ, clust_no), sr in df.groupby(['organ','clust_no']).gene:
    print(organ, clust_no)
    sub_df = utils.z_score(data_df[organ].loc[sr])
    sr = sub_df.groupby(axis=1,level=0,sort=False).apply(calc_max_eigval)
    sr.name = f'{organ}-c{clust_no}'

    if False:
      alpha = 0.2
      sr.iloc[:] = signal.convolve(sr, [alpha,1-2*alpha,alpha], mode='same')

    out_list.append(sr)
  df = pd.concat(out_list, axis=1).T
  sr = df.apply(np.argmax, axis=1).sort_values()
  df = df.loc[sr.index]
  vmax = df.max().max() * 1.2

  fig, ax = plt.subplots(figsize=(6,5))
  g = sns.heatmap(df, cmap='Blues', ax=ax, yticklabels=1, mask=df.isnull(),
                  cbar_kws=dict(label='maximum eigenvalue',
                                shrink=0.6, aspect=10), vmin=0, vmax=vmax)
  g.set_facecolor('0.8')
  ax.tick_params(length=0)
  ax.set_xlabel(None)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
  cb = ax.collections[0].colorbar
  cb.outline.set_linewidth(1)
  cb.ax.tick_params(length=1, width=2)
  for i, j in enumerate(sr):
    ax.text(j+0.5, i+0.5, 'x', ha='center', va='center')
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df

if __name__ == '__main__':
  hoge = plot_max_eigval(data_df)
