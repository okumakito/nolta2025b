def plot_overlap2():
  file_name1 = '../data/sfg/sfg_summary_gene.csv'
  file_name2 = '../../koizumi_tsod13/data/sfg_noctrl/sfg_noctrl_summary_gene.csv'
  #file_name2 = '../../koizumi_tsod13/data/bleg_noctrl/bleg_noctrl_summary_gene.csv'
  #file_name2 = '../../koizumi_tsod13/data/sfg_noctrl_prev/sfg_noctrl_prev_summary_gene.csv'
  #file_name2 = '../../koizumi_tsod13/data/bleg_noctrl_prev/bleg_noctrl_prev_summary_gene.csv'
  #file_name2 = '../data/deg/deg_summary_gene.csv'
  axis_label1, axis_label2 = 'B6 mouse SFG', 'TSOD mouse SFG'
  #axis_label1, axis_label2 = 'SFGs', 'DEGs'

  df1 = pd.read_csv(file_name1)
  df2 = pd.read_csv(file_name2)
  df1['label'] = df1.organ + df1.clust_no.astype(str)
  df2['label'] = df2.organ + df2.clust_no.astype(str)
  out_list = []
  for label1, sr1 in df1.groupby('label').gene:
    for label2, sr2 in df2.groupby('label').gene:
      n = np.intersect1d(sr1, sr2).size
      cup = np.union1d(sr1, sr2).size
      jac = n / cup
      out_list.append(dict(label1=label1, label2=label2, n=n, jac=jac))
  df = pd.DataFrame(out_list)
  n_df   = df.set_index(['label1','label2']).n.unstack()
  jac_df = df.set_index(['label1','label2']).jac.unstack()

  if False:
    Z = linkage(jac_df, method='ward', metric='euclidean')
    Z2 = linkage(jac_df.T, method='ward', metric='euclidean')
    i_arr = leaves_list(Z)
    j_arr = leaves_list(Z2)
    jac_df = jac_df.iloc[i_arr, j_arr]

  fig, ax = plt.subplots(figsize=(10,7))
  sns.heatmap(jac_df, ax=ax, cmap='Blues', xticklabels=1, yticklabels=1,
              cbar_kws=dict(label='Jaccard index', shrink=0.5, aspect=10))
  ax.tick_params(length=0)
  ax.set_xlabel(axis_label2, fontsize=16)
  ax.set_ylabel(axis_label1, fontsize=16)
  ax.set_aspect('equal')
  ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
  cb = ax.collections[0].colorbar
  cb.ax.tick_params(length=2, width=1)
  cb.outline.set_linewidth(1)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(2)
  for i in 4 * (np.arange(jac_df.shape[0] // 4)+1):
    ax.axhline(i,c='k',lw=1)
  for i in 4 * (np.arange(jac_df.shape[1] // 4)+1):
    ax.axvline(i,c='k',lw=1)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return jac_df

if __name__ == '__main__':
  hoge = plot_overlap2()
