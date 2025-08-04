def plot_pca_all(data_df):
  df = data_df.copy()
  df = df[df.min(axis=1)>5]
  model = PCA(n_components=2, random_state=0)
  pos_df = pd.DataFrame(model.fit_transform(df.T), columns=list('xy'))
  pos_df['organ'] = df.columns.get_level_values(0)
  
  fig, ax = plt.subplots(figsize=(6,5))
  sns.scatterplot(data=pos_df, x='x', y='y', hue='organ', ax=ax,
                  palette='tab20', s=5, ec='none')
  ax.legend(bbox_to_anchor=(1,1), frameon=False, handletextpad=0,
            loc='upper left')
  ax.margins(0.1)
  ax.tick_params(length=5)
  perc1, perc2 = 100 * model.explained_variance_ratio_
  ax.set_xlabel(f'PC1 ({perc1:.1f} %)')
  ax.set_ylabel(f'PC2 ({perc2:.1f} %)')
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  plot_pca_all(data_df)
