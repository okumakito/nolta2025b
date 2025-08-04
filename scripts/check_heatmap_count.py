def check_heatmap_count(count_df, organ):
  df = count_df.T[count_df.columns.str.startswith(organ)].T
  df = (df+1).apply(np.log2)
  n = 600
  yticklabels=15
  vmax = 25
  vmin = 0
  sr = pd.Series(df.index,
                 index=(np.arange(len(df)) / n).astype(int)+1)
  for i in sr.index.unique()[:]:
    print(i)
    sub_df = df.loc[sr[i]]
    fig, ax = plt.subplots(figsize=(6,6))
    sns.heatmap(sub_df, cmap='viridis', ax=ax, vmax=vmax, vmin=vmin,
                yticklabels=yticklabels, xticklabels=False,
                cbar_kws=dict(label='log2 (count + 1)'))
    ax.tick_params(length=0)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=9)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_title(f'{organ} {i}')
    cb = ax.collections[0].colorbar
    cb.ax.tick_params(length=2, width=1)
    cb.outline.set_linewidth(1)
    fig.tight_layout(pad=0)
    fig.savefig(f'tmp_{organ}_{i:02d}.png')
    plt.close()

if __name__ == '__main__':
  if 'count_df' not in locals():
    count_df = load_data_count()
  organ = sys.argv[1]
  check_heatmap_count(count_df, organ)
