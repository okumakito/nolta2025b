def plot_overlap3_nolta():
  data_file = '../data/sfg/sfg_summary_gene.csv'
  rename_file = '../data/rename_list.csv'
  organ_list = ['ewat','iwat','bat','liver','gas','panc','gut','hypo','pit']
  n_organ = len(organ_list)
  df = pd.read_csv(data_file)
  df = df[df.clust_no==1]
  df = df[df.organ.isin(organ_list)]
  rename_sr = pd.read_csv(rename_file, index_col=0).squeeze()
  df['label'] = df.organ.replace(rename_sr)
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
    n_df = n_df.iloc[i_arr, i_arr]

  np.fill_diagonal(jac_df.values, 0)

  fig, ax = plt.subplots(figsize=(7,6))
  sns.heatmap(jac_df, ax=ax, cmap='Blues', xticklabels=1, yticklabels=1,
              cbar_kws=dict(label='Jaccard index', shrink=0.5, aspect=10))
  th = 50
  mask_diag = pd.DataFrame(np.eye(n_organ), index=n_df.index,
                          columns=n_df.columns).astype(bool)
  sns.heatmap(n_df, ax=ax, annot=True, alpha=0, annot_kws=dict(c='k'),
              cbar=False, fmt='d', mask=(n_df>=th) | mask_diag)
  sns.heatmap(n_df, ax=ax, annot=True, alpha=0, annot_kws=dict(c='w'),
              cbar=False, fmt='d', mask=(n_df<th) | mask_diag)
  ax.tick_params(length=0, pad=5)
  ax.set_xlabel(None)
  ax.set_ylabel(None)
  ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
  ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
  cb = ax.collections[0].colorbar
  cb.ax.tick_params(length=3, width=1)
  cb.outline.set_linewidth(1)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
  # for i in 3 * (np.arange(n_organ // 3)+1):
  #   ax.axhline(i,c='k',lw=1)
  # for i in 3 * (np.arange(n_organ // 3)+1):
  #   ax.axvline(i,c='k',lw=1)
  ax.plot([0,n_organ], [0, n_organ], 'k-', lw=1)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return jac_df

if __name__ == '__main__':
  hoge = plot_overlap3_nolta()
