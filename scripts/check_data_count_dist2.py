def check_data_count_dist2(sol_df):
  info_file = '../data/gene_info.csv'
  df = sol_df.copy()
  df2 = pd.read_csv(info_file, usecols=['start','end','gene_sym'],
                    index_col='gene_sym')
  len_sr = (df2.end - df2.start).groupby(level=0).max()
  len_sr = len_sr[df.index]
  df_adj = df.divide(len_sr, axis=0)
  df     = df.apply(np.log2)
  df_adj = df_adj.apply(np.log2)
  
  sr  = df.iloc[:, :10].mean(axis=1)    # many zeros
  sr2 = df.iloc[:, 25:75].mean(axis=1)  # normal
  sr3 = df_adj.iloc[:, :10].mean(axis=1)
  sr4 = df_adj.iloc[:, 25:75].mean(axis=1)

  def func(sr, sr2, ax, title):
    kws = dict(kde=False, bins=50)
    sns.distplot(sr, ax=ax, **kws)
    sns.distplot(sr2, ax=ax, **kws)
    ax.tick_params(length=0)
    ax.set_title(title)
  
  fig, axes = plt.subplots(figsize=(8,8), nrows=4, ncols=2)

  ax = axes[0,0]
  func(sr, sr2, ax, 'all')

  ax = axes[1,0]
  idx = len_sr[len_sr<2000].index
  func(sr[idx], sr2[idx], ax, 'less than 2000')

  ax = axes[2,0]
  idx = len_sr[(len_sr>=2000) & (len_sr<10000)].index
  func(sr[idx], sr2[idx], ax, '2000 to 10000')

  ax = axes[3,0]
  idx = len_sr[len_sr>=10000].index
  func(sr[idx], sr2[idx], ax, 'greater than 10000')

  ax = axes[0,1]
  func(sr3, sr4, ax, 'adj, all')

  ax = axes[1,1]
  idx = len_sr[len_sr<2000].index
  func(sr3[idx], sr4[idx], ax, 'adj, less than 2000')

  ax = axes[2,1]
  idx = len_sr[(len_sr>=2000) & (len_sr<10000)].index
  func(sr3[idx], sr4[idx], ax, 'adj, 2000 to 10000')

  ax = axes[3,1]
  idx = len_sr[len_sr>=10000].index
  func(sr3[idx], sr4[idx], ax, 'adj, greater than 10000')

  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

  # diff
  df_out = (sr3 - sr4).round(3).to_frame('fc')
  df_out['length'] = len_sr[df_out.index]
  df_out = df_out.dropna().sort_values('fc', ascending=False)
  df_out.to_csv('tmp.csv')
  return  df_out

if __name__ == '__main__':
  if 'sol_df' not in locals():
    sol_df = load_sol_df()
  hoge = check_data_count_dist2(sol_df)
