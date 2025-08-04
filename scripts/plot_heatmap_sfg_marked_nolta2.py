def calc_max_eigval(df_in):
  n = df_in.shape[1]
  df = df_in.rank(axis=1).T * utils.mad(df_in)
  df /= (n*(n+1)/12)**0.5
  return np.linalg.eigvalsh(df.cov()).max()

def func(df_in):
  n = df_in.shape[1]
  df = df_in.rank(axis=1).T * utils.mad(df_in)
  df /= (n*(n+1)/12)**0.5
  return (df - df.mean()).T

def plot_heatmap_sfg_marked_nolta2(data_df):
  sfg_file = '../data/sfg/sfg_summary_gene.csv'
  rename_file = '../data/rename_list.csv'
  sfg_df = pd.read_csv(sfg_file)
  sfg_df = sfg_df[sfg_df.clust_no==1]
  rename_sr = pd.read_csv(rename_file, index_col=0).squeeze()
  organ_list = ['hypo','gut','ewat','bat','pit','iwat','panc','gas','liver']

  fig, axes = plt.subplots(figsize=(12,9), ncols=3, nrows=4,
                           gridspec_kw=dict(height_ratios=[1,1,1,0.15]))
  axes = axes.flatten()
  cax = axes[10]

  for i, (organ, ax) in enumerate(zip(organ_list, axes)):
    gene_sr = sfg_df[sfg_df.organ==organ].gene
    df = utils.z_score(data_df[organ].loc[gene_sr])
    sr = df.groupby(axis=1,level=0,sort=False).apply(calc_max_eigval)
    idx = np.argmax(sr)
    df = df.groupby(axis=1,level=0,sort=False).apply(func)
    n = len(df)
    cmap = 'PiYG_r'
    if i==8:
      sns.heatmap(df, cmap=cmap, ax=ax, yticklabels=False, cbar=True,
                  vmin=-2, vmax=2, cbar_ax=cax,
                  cbar_kws=dict(label='normalized gene expression',
                                orientation='horizontal'))
    else:
      sns.heatmap(df, cmap=cmap, ax=ax, yticklabels=False, cbar=False,
                  vmin=-2, vmax=2)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_title(f'{rename_sr[organ]} ({n} genes, {sr.index[idx]})',
                 fontsize=16, pad=10)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
      spine.set_visible(True)
      spine.set_linewidth(1)

    sr = df.groupby(axis=1,level=0,sort=False).count().iloc[0]
    for i in sr.cumsum()[:-1]:
      ax.axvline(i, lw=1, c='k')

    i  = sr.cumsum().iat[idx]
    i2 = sr.cumsum().iat[idx-1] if idx else 0
    ax.plot([i,i,i2,i2,i], [0,n,n,0,0], lw=3, c='0.2')
    ax.set_xticks(sr.cumsum() - sr/2)
    ax.set_xticklabels(sr.index)

  cax.tick_params(length=5, width=1)
  for spine in cax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
  axes[9].axis('off')
  axes[11].axis('off')
  fig.tight_layout(h_pad=2, w_pad=2)

  # arrows, &
  for i in [0,1,6]:
    axes[i].text(1.02, 0.5, '\u21e8', transform=axes[i].transAxes,
                 ha='left', va='center', fontsize=30)
  for i in [3,4]:
    axes[i].text(1.02, 0.5, '\u21e6', transform=axes[i].transAxes,
                 ha='left', va='center', fontsize=30)
  for i in [2,3]:
    axes[i].text(0.5, -0.3, '\u21e9', transform=axes[i].transAxes,
                 ha='center', va='top', fontsize=30)
  for i in [7]:
    axes[i].text(1.02, 0.5, '&', transform=axes[i].transAxes,
                 ha='left', va='center', fontsize=24)

  fig.show()
  fig.savefig('tmp.png')
  return df

if __name__ == '__main__':
  hoge = plot_heatmap_sfg_marked_nolta2(data_df)
