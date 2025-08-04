def check_data_norm_dist(df_in):
  file_name = '../data/data_norm.csv'
  if df_in is None:
    df = pd.read_csv(file_name, index_col=0)
    df.columns = df.columns.str.split('_').str[0]
    df = df[df.columns.unique().sort_values()]
    sr = df.columns.to_series()
  else:
    df = df_in.copy()
    sr = df.columns.get_level_values(0).to_series()

  fig ,axes = plt.subplots(figsize=(8,7), nrows=2)

  # zero ratio
  ax = axes[0]
  ax.plot((df==0).mean().values, '.')
  ax.set_ylabel('zero ratio')

  # quartile
  ax = axes[1]
  df[df==0] = None
  ax.plot(df.quantile(0.75).values, '.', label='75 %')
  ax.plot(df.median().values, '.', label='50 %')
  ax.plot(df.quantile(0.25).values, '.', label='25 %')
  ax.set_ylabel('log expression')
  ax.legend(bbox_to_anchor=(1,1), frameon=False, markerscale=2,
            handletextpad=0, borderaxespad=0)

  for ax in axes:
    ax.tick_params(length=5)
    ax.margins(0.02, 0.05)
    n_sr = sr.groupby(level=0, sort=False).count()
    ax.set_xticks(n_sr.cumsum() - n_sr/2)
    ax.set_xticklabels(n_sr.index, rotation=90)
    for i, j in zip(n_sr.cumsum()[:-1:2], n_sr.cumsum()[1::2]):
      ax.axvspan(i, j, color='k', alpha=0.1, lw=0)

  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  #check_data_norm_dist(None)
  check_data_norm_dist(data_df)
