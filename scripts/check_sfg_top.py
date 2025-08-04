def check_sfg_top(data_df, organ):
  file_name1 = '../data/sfg/sfg_summary_gene.csv'
  file_name2 = '../data/sfg/sfg_summary_gene_nolta.csv'

  fig, axes = plt.subplots(figsize=(6,6), nrows=2)
  for ax, file_name in zip(axes, [file_name1, file_name2]):
    df = pd.read_csv(file_name)
    sr = df[df.organ==organ].head(10).gene
    print('mean:', data_df.loc[sr,organ].T.mean().mean())
    print('std:', data_df.loc[sr,organ].T.std().mean())
    df2 = utils.z_score(data_df.loc[sr,organ])
    sns.heatmap(data=df2, cmap='RdBu_r', vmax=3, vmin=-3, ax=ax,
                yticklabels=1, xticklabels=False)
    ax.tick_params(length=0)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    cb = ax.collections[0].colorbar
    cb.ax.tick_params(length=3, width=1)
    cb.outline.set_linewidth(1)
  fig.suptitle(organ, fontsize=16)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  organ = sys.argv[1]
  check_sfg_top(data_df, organ)
