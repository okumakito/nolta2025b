def check_rpl_rps4(count_df):
  idx = count_df.index
  rp_idx = idx[idx.str.startswith('Rpl') | idx.str.startswith('Rps')]
  sr =  count_df.loc[rp_idx].sum() / count_df.sum()
  sr.index = sr.index.str.split('_').str[0]
  df = sr.groupby(level=0).apply(lambda x:x.reset_index(drop=True)).unstack()
  vmax = df.max().max()

  fig, ax = plt.subplots(figsize=(6,4))
  g = sns.heatmap(df, cmap='Blues', ax=ax, vmin=0, vmax=vmax,
                  mask=df.isnull())
  ax.set_title('RP proportion', fontsize=16, pad=10)
  ax.tick_params(length=0)
  ax.set_xlabel('samples')
  g.set_facecolor('0.8')
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
  cb = ax.collections[0].colorbar
  cb.outline.set_linewidth(1)
  cb.ax.tick_params(length=2, width=1)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df

if __name__ == '__main__':
  if 'count_df' not in locals():
    count_df = load_data_count()
  hoge = check_rpl_rps4(count_df)
