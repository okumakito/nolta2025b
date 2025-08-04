def check_skew3(data_df, organ):
  df = data_df[organ].copy()
  df = df[df.mean(axis=1)>5]
  df = df[df.min(axis=1)>0]
  mean_df = df.groupby(axis=1,level=0).mean()
  sr = mean_df.max(axis=1) - mean_df.min(axis=1)
  df = df[sr > 1]
  df = utils.z_score(df)
  Z = linkage(df, method='average', metric='correlation')
  df = df.iloc[leaves_list(Z)]

  fig, ax = plt.subplots(figsize=(6,4))
  sns.heatmap(df, cmap='RdBu_r', vmax=3, vmin=-3, ax=ax,
              xticklabels=False, yticklabels=False,
              cbar_kws=dict(label='z score'))
  ax.tick_params(length=0)
  ax.set_title(organ, fontsize=16, pad=10)
  ax.set_xlabel(f'{df.shape[1]} samples')
  ax.set_ylabel(f'{len(df)} DEGs')
  cb = ax.collections[0].colorbar
  cb.ax.tick_params(length=2, width=1)
  cb.outline.set_linewidth(1)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  organ = sys.argv[1]
  check_skew3(data_df, organ)
