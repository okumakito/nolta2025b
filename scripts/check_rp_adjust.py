def check_rp_adjust(norm_df, adj_df, organ):
  df1 = norm_df.T[norm_df.columns.str.startswith(organ)].T
  df2 = adj_df.T[adj_df.columns.str.startswith(organ)].T
  vmax = 40

  fig, axes = plt.subplots(figsize=(10,8), ncols=2)
  label_list = [f'{organ} original',f'{organ} adjusted']

  for ax, df, label in zip(axes, [df1, df2], label_list):
    sns.heatmap(df, cmap='viridis', ax=ax, xticklabels=False,
                yticklabels=False, vmax=vmax, vmin=0,
                cbar_kws=dict(label='log expression', pad=0.1,
                              orientation='horizontal'))
    ax.set_xlabel('samples')
    ax.set_ylabel('genes')
    ax.set_title(label, fontsize=16, pad=10)
    ax.tick_params(length=0)
    cb = ax.collections[0].colorbar
    cb.ax.tick_params(length=3, width=1)

  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df2

if __name__ == '__main__':
  organ = sys.argv[1]
  if 'norm_df' not in locals():
    norm_df = pd.read_csv('../data/data_norm.csv', index_col=0)
  if 'adj_df' not in locals():
    adj_df = pd.read_csv('../data/data_norm_adj_noremove.csv', index_col=0)
  hoge = check_rp_adjust(norm_df, adj_df, organ)
