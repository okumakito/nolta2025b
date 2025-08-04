from umap import UMAP
def plot_pca_all_nolta(data_df):
  df = data_df.copy()
  df = df[df.min(axis=1)>5]
  model     = PCA(n_components=2, random_state=0)
  model2    = UMAP(random_state=0, init='pca', min_dist=5, spread=5)
  organ_idx = df.columns.get_level_values(0)
  sr = pd.read_csv('../data/rename_list.csv', index_col=0).squeeze()

  def func(model):
    df2 = pd.DataFrame(model.fit_transform(df.T), columns=list('xy'),
                          index=organ_idx)
    df2.index = df2.index.to_series().replace(sr)
    df2 = df2.loc[sr.values]
    return df2
  pos_df  = func(model)
  pos_df2 = func(model2)

  fig, axes = plt.subplots(figsize=(12,5), ncols=2)

  ax = axes[0]
  sns.scatterplot(data=pos_df, x='x', y='y', hue='organ', ax=ax,
                  palette='tab20', s=10, ec='none', legend=False)
  ax.margins(0.1)
  ax.tick_params(length=5)
  perc1, perc2 = 100 * model.explained_variance_ratio_
  ax.set_xlabel(f'PC1 ({perc1:.1f}%)')
  ax.set_ylabel(f'PC2 ({perc2:.1f}%)')
  ax.text(-0.18, 1, 'A', fontsize=20, transform=ax.transAxes,
          ha='right', va='top')

  ax = axes[1]
  sns.scatterplot(data=pos_df2, x='x', y='y', hue='organ', ax=ax,
                  palette='tab20', s=10, ec='none')
  ax.legend(bbox_to_anchor=(1,1), frameon=False, handletextpad=0,
            loc='upper left', markerscale=4)
  ax.tick_params(length=5)
  ax.set_xlabel('UMAP axis 1')
  ax.set_ylabel('UMAP axis 2')
  ax.text(-0.15, 1, 'B', fontsize=20, transform=ax.transAxes,
          ha='right', va='top')

  fig.tight_layout(w_pad=2)
  fig.show()
  fig.savefig('tmp.png')
  return pos_df

if __name__ == '__main__':
  hoge = plot_pca_all_nolta(data_df)
