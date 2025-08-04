def plot_rp(count_df, organ):
  df = count_df.T[count_df.columns.str.startswith(organ)].T.copy()
  idx = df.index
  rp_idx = idx[idx.str.startswith('Rpl') | idx.str.startswith('Rps')]
  print(rp_idx.size)
  rp_df  = df.loc[rp_idx]
  df2    = (df+1).apply(np.log2)
  rp_df2 = (rp_df+1).apply(np.log2)

  fig, axes = plt.subplots(figsize=(10,8), nrows=2, ncols=2,
                           gridspec_kw=dict(height_ratios=[0.5,1]))

  ax = axes[0,0]
  sr = rp_df.sum() / df.sum()
  ax.plot(sr.values)
  ax.set_xlabel('sample')
  ax.tick_params(length=5)
  ax.set_ylabel('RP proportion')
  ax.set_ylim((0, 1.1 * sr.max()))

  ax = axes[0,1]
  ax.set_axis_off()
  ax.set_ylim((0,4))
  ax.text(0, 3, organ, fontsize=30)
  ax.text(0, 2, f'mean = {sr.mean():.04f}')
  ax.text(0, 1, f'std = {sr.std():.04f}')
  ax.text(0, 0, f'cv = {sr.std()/sr.mean():.03f}')
  
  ax = axes[1,0]
  sns.heatmap(rp_df2, cmap='viridis', ax=ax, xticklabels=False,
              cbar_kws=dict(label='log2 (count + 1)'))
  ax.tick_params(length=0)
  ax.set_xlabel('samples')
  ax.set_ylabel(None)
  cb = ax.collections[0].colorbar
  cb.outline.set_linewidth(1)
  cb.ax.tick_params(length=2, width=1)

  ax = axes[1,1]
  sns.heatmap(df2, cmap='viridis', ax=ax, xticklabels=False,
              yticklabels=False,
              cbar_kws=dict(label='log2 (count + 1)'))
  ax.tick_params(length=0)
  ax.set_xlabel('samples')
  ax.set_ylabel(f'all {len(df2)} genes')
  cb = ax.collections[0].colorbar
  cb.outline.set_linewidth(1)
  cb.ax.tick_params(length=2, width=1)

  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return rp_df

if __name__ == '__main__':
  if 'count_df' not in locals():
    count_df = load_data_count()
  organ = sys.argv[1]
  hoge = plot_rp(count_df, organ)
