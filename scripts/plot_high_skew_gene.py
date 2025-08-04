def plot_high_skew_gene():
  file_name = '../data/high_skew_gene_example.csv'
  df = pd.read_csv(file_name, usecols=range(7), dtype=str)
  sr = df.gene_sym.fillna('unknown') + '\n' + df['chr'] \
      + ':' + df.start + '-' + df.end
  df = pd.read_csv(file_name).iloc[:,7:].copy()
  df.index = [np.repeat(np.arange(5),2), sr.values]

  fig, axes = plt.subplots(figsize=(10,8), nrows=5)
  for (i, sub_df), ax in zip(df.groupby(axis=0,level=0), axes):
    df2 = sub_df.copy()
    df2.index = df2.index.droplevel(0)
    df2.T.plot(kind='bar', stacked=True, ax=ax, width=0.8)
    xticks = np.arange(df2.shape[1])[::4]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks.astype(str))
    ax.tick_params(length=5)
    ax.legend(bbox_to_anchor=(1,1), frameon=False)
    ax.set_ylabel('count')
  axes[-1].set_xlabel('sample number')
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df

if __name__ == '__main__':
  hoge = plot_high_skew_gene()
