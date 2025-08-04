def plot_heatmap(data_df, res_df, organ, title):
  df = utils.z_score(data_df.loc[res_df.gene, organ])
  #vmax = df.abs().quantile(0.99).max()
  vmax = 4
  fig, ax = plt.subplots(figsize=(6,5))
  sns.heatmap(df, cmap='RdBu_r', ax=ax, vmin=-vmax, vmax=vmax,
              cbar_kws=dict(label='z-score'))
  ax.set_xlabel(None)
  ax.set_ylabel(None)
  ax.set_title(organ + ' ' + title, fontsize=16, pad=10)
  ax.tick_params(length=0)
  cb = ax.collections[0].colorbar
  cb.ax.tick_params(length=2, width=1)
  cb.outline.set_linewidth(1)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)

  sr = res_df.clust.value_counts()
  for i in sr.cumsum()[:-1]:
    ax.axhline(i, lw=1, c='k')
  ax.set_yticks(sr.cumsum() - sr/2)
  ax.set_yticklabels('c' + sr.index.astype(str))

  sr = df.groupby(axis=1,level=0, sort=False).count().iloc[0]
  for i in sr.cumsum()[:-1]:
    ax.axvline(i, lw=1, c='k')
  df2 = sr.index.to_frame()
  ax.set_xticks(sr.cumsum() - sr/2)
  ax.set_xticklabels(df2.time)

  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  organ = sys.argv[1]
  title = sys.argv[2]
  plot_heatmap(data_df, res_df, organ, title)
