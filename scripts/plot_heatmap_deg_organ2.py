def plot_heatmap_deg_organ2(data_df, res_df, organ):
  df = data_df.loc[res_df[res_df.organ==organ].gene_symbol]
  df = df.groupby(axis=1, level=0).mean()
  df = utils.z_score(df)

  fig, ax = plt.subplots(figsize=(4,4))
  sns.heatmap(df, ax=ax, cmap='RdBu_r', vmax=3, vmin=-3,
              xticklabels=1, yticklabels=False,
              cbar_kws=dict(label='z-score'))
  ax.set_xlabel(None)
  ax.set_ylabel(f'top {len(df)} genes')
  ax.tick_params(length=0)
  ax.set_title(organ, pad=10, fontsize=16)
  cb = ax.collections[0].colorbar
  cb.ax.tick_params(length=2, width=1)
  cb.outline.set_linewidth(1)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)

  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df

if __name__ == '__main__':
  organ = sys.argv[1]
  hoge = plot_heatmap_deg_organ2(data_df, res_df, organ)
