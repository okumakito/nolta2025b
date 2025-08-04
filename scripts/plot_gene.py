# NOTE: use data_norm_adj_noremove.csv
def plot_gene(data_df, gene):
  df = data_df.loc[gene].groupby(level=0,sort=False).\
      apply(lambda x:x.reset_index(drop=True)).unstack()
  n_sr = data_df.ewat.columns.to_series().groupby(level=0,sort=False).count()
  fig, ax = plt.subplots(figsize=(9,4))
  g = sns.heatmap(df, cmap='Blues', ax=ax, vmin=0,
                  cbar_kws=dict(label='log expression', aspect=15))
  g.set_facecolor('0.8')
  ax.tick_params(length=0)
  ax.set_xlabel(None)
  ax.set_ylabel(None)
  ax.set_title(gene, fontsize=16, pad=10)
  ax.set_xticks(n_sr.cumsum() - n_sr/2)
  ax.set_xticklabels(n_sr.index, rotation=0)
  for i in n_sr.cumsum()[:-1]:
    ax.axvline(i, c='k', lw=1)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
  cb = ax.collections[0].colorbar
  cb.outline.set_linewidth(1)
  cb.ax.tick_params(length=2, width=1)
  fig.tight_layout()
  fig.show()
  return df

if __name__ == '__main__':
  gene = sys.argv[1]
  hoge = plot_gene(data_df, gene)
