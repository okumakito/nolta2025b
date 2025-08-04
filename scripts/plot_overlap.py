def plot_overlap():
  deg_file_name = '../data/deg/deg_summary_gene.csv'
  sfg_file_name = '../data/sfg/sfg_summary_gene.csv'
  df1 = pd.read_csv(deg_file_name)
  df2 = pd.read_csv(sfg_file_name)
  df1['label'] = 'deg-' + df1.organ + df1.clust_no.astype(str)
  df2['label'] = 'sfg-' + df2.organ + df2.clust_no.astype(str)
  #df = df1
  #df = df2
  df = pd.concat([df1, df2], axis=0)
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

  fig, ax = plt.subplots(figsize=(10,9))
  sns.heatmap(jac_df, ax=ax, cmap='Blues', xticklabels=1, yticklabels=1,
              cbar_kws=dict(label='Jaccard index', shrink=0.5))
  ax.tick_params(length=0)
  ax.set_xlabel(None)
  ax.set_ylabel(None)
  cb = ax.collections[0].colorbar
  cb.ax.tick_params(length=2, width=1)
  cb.outline.set_linewidth(1)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return jac_df

if __name__ == '__main__':
  hoge = plot_overlap()
