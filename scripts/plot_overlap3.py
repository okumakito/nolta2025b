def plot_overlap3(file_name, title):
  df = pd.read_csv(file_name)
  if 'clust_no' in df.columns:
    df['label'] = df.organ + '-c' + df.clust_no.astype(str)
  else:
    df['label'] = df.organ
  out_list = []
  for label1, sr1 in df.groupby('label').gene:
    for label2, sr2 in df.groupby('label').gene:
      n = np.intersect1d(sr1, sr2).size
      cup = np.union1d(sr1, sr2).size
      jac = n / cup
      out_list.append(dict(label1=label1, label2=label2, n=n, jac=jac))
  df = pd.DataFrame(out_list)
  n_df   = df.set_index(['label1','label2']).n.unstack()
  jac_df = df.set_index(['label1','label2']).jac.unstack()

  if True:
    d_arr = distance.squareform(1-jac_df)
    Z = linkage(d_arr, method='ward', metric='euclidean')
    i_arr = leaves_list(Z)
    jac_df = jac_df.iloc[i_arr, i_arr]

  np.fill_diagonal(jac_df.values, 0)

  fig, ax = plt.subplots(figsize=(8,7))
  sns.heatmap(jac_df, ax=ax, cmap='Blues', xticklabels=1, yticklabels=1,
              cbar_kws=dict(label='Jaccard index', shrink=0.5, aspect=10))
  ax.tick_params(length=0)
  ax.set_xlabel(None)
  ax.set_ylabel(None)
  ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
  ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
  ax.set_title(title, fontsize=16, pad=10)
  cb = ax.collections[0].colorbar
  cb.ax.tick_params(length=2, width=1)
  cb.outline.set_linewidth(1)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
  for i in 4 * (np.arange(jac_df.shape[0] // 4)+1):
    ax.axhline(i,c='k',lw=1)
  for i in 4 * (np.arange(jac_df.shape[1] // 4)+1):
    ax.axvline(i,c='k',lw=1)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return jac_df

if __name__ == '__main__':
  file_name = sys.argv[1]  # ex. ../data/deg_organ/deg_organ_summary_gene.csv
  title = sys.argv[2]
  hoge = plot_overlap3(file_name, title)
