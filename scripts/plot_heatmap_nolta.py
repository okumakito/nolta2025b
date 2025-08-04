def calc_max_eigval(df_in):
  n = df_in.shape[1]
  df = df_in.rank(axis=1).T * utils.mad(df_in)
  df /= (n*(n+1)/12)**0.5
  return np.linalg.eigvalsh(df.cov()).max()

def plot_heatmap_nolta(data_df, res_df, organ):
  df = utils.z_score(data_df.loc[res_df[res_df.clust==1].gene, organ])
  sr_score = df.groupby(axis=1,level=0,sort=False).apply(calc_max_eigval)
  idx = sr_score.idxmax()
  vmax = 4
  fig, axes = plt.subplots(figsize=(4,8), nrows=2,
                           gridspec_kw=dict(height_ratios=[6,2]))
  ax = axes[0]
  sns.heatmap(df, cmap='RdBu_r', ax=ax, vmin=-vmax, vmax=vmax,
              cbar_kws=dict(label='z-score', orientation='horizontal',
                            shrink=0.8, pad=0.15))
  ax.set_xlabel(None)
  ax.set_ylabel(f'{len(df)} genes', labelpad=10)
  ax.tick_params(length=0)
  cb = ax.collections[0].colorbar
  cb.ax.tick_params(length=2, width=1)
  cb.outline.set_linewidth(1)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
  sr = df.groupby(axis=1,level=0, sort=False).count().iloc[0]
  for i in sr.cumsum()[:-1]:
    ax.axvline(i, lw=1, c='k')
  df2 = sr.index.to_frame()
  ax.set_xticks(sr.cumsum() - sr/2)
  ax.set_xticklabels(df2.time)
  ax.set_yticks([])
  ax.text(-0.08, 1, 'A', fontsize=20, transform=ax.transAxes,
          ha='right', va='top')

  ax = axes[1]
  ax.plot(sr_score, 'o-')
  ax.set_title('fluctuation strength')
  ax.set_ylabel(None)
  ax.set_xticks(np.arange(sr.size), sr.index, rotation=90)
  ax.set_ylim((0, 1.2 * sr_score.max()))
  ax.tick_params(length=5, width=1)
  for spine in ax.spines.values():
    spine.set_linewidth(1)
  ax.scatter([idx], [sr_score[idx]], s=150, c='C3', zorder=10)
  ax.text(-0.08, 1, 'B', fontsize=20, transform=ax.transAxes,
          ha='right', va='bottom')

  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  organ = sys.argv[1]
  plot_heatmap_nolta(data_df, res_df, organ)
