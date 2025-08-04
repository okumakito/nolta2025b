def plot_pca_organ(data_df):
  organ_idx = data_df.columns.get_level_values(0).unique()
  model = PCA(n_components=2, random_state=0)
  fig, axes = plt.subplots(figsize=(12,9), nrows=3, ncols=5)
  axes = axes.flatten()
  for organ, ax in zip(organ_idx, axes):
    df = data_df[organ].loc[:,:'12w'].copy()
    #df = df[df.median(axis=1)>0]
    df = df[df.min(axis=1)>5]
    #df = utils.z_score(df)
    if False:
      df2 = df.groupby(axis=1,level=0).mean()
      sr = df2.max(axis=1) - df2.min(axis=1)
      print(df.shape)
      df = df[sr > 2]
      print(df.shape)
    pos_df = pd.DataFrame(model.fit_transform(df.T), columns=list('xy'))
    # sign change: left > right, top > bottom
    corr_df = pos_df.reset_index().corr()
    pos_df *= corr_df.iloc[0, 1:].apply(np.sign) * [1,-1]
    pos_df['time'] = df.columns

    sns.scatterplot(data=pos_df, x='x', y='y', hue='time', ax=ax,
                    palette='magma', ec='none')
    ax.legend_.remove()
    ax.set_title(organ, fontsize=16, pad=10)
    ax.margins(0.1)
    ax.tick_params(length=5)
    perc1, perc2 = 100 * model.explained_variance_ratio_
    ax.set_xlabel(f'PC1 ({perc1:.1f} %)')
    ax.set_ylabel(f'PC2 ({perc2:.1f} %)')
    ax.set_xticks([])
    ax.set_yticks([])

  for ax in axes[organ_idx.size:]:
    ax.axis('off')

  # show legend
  axes[4].legend(bbox_to_anchor=(1,0.5), frameon=False, handletextpad=0,
                 loc='center left', labelspacing=0, borderaxespad=0)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  plot_pca_organ(data_df)
