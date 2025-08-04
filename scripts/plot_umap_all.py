from umap import UMAP
def plot_umap_all(data_df):
  model = PCA(n_components=20, random_state=0)
  X = model.fit_transform(data_df.T)
  model = UMAP(random_state=0, init=X[:,:2], min_dist=5, spread=5)
  if False:
    pos_arr = model.fit_transform(X) # 20-dim
  else:
    pos_arr = model.fit_transform(data_df.T) # original
  df = pd.DataFrame(pos_arr, index=data_df.columns, columns=list('xy'))

  # sort by axis 2
  organ_idx = df.groupby(axis=0, level=0).mean().y.sort_values().index[::-1]

  fig, ax = plt.subplots(figsize=(6,5))

  if False: # organ
    color_list = [plt.cm.tab20(i) for i in range(13)]
    for color, organ in zip(color_list, organ_idx):
      sub_df = df.loc[organ]
      ax.scatter(sub_df.x, sub_df.y, label=organ, s=5, color=color)
  else: # week
    week_arr = data_df.columns.get_level_values(1).unique()
    n = len(week_arr)
    color_list = [plt.cm.viridis(i/n) for i in range(n)]
    for color, week in zip(color_list, week_arr):
      sub_df = df.xs(week, axis=0, level=1)
      ax.scatter(sub_df.x, sub_df.y, label=str(week), s=5, color=color)
      
  ax.legend(markerscale=4, handletextpad=0, bbox_to_anchor=(1,0.5),
            loc='center left', frameon=False)
  ax.set_xlabel('UMAP axis 1')
  ax.set_ylabel('UMAP axis 2')
  ax.tick_params(length=5)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  hoge = plot_umap_all(data_df)
