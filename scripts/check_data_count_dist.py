def load_sol_df():
  file_name = '../data/data_count.csv'
  df = pd.read_csv(file_name, index_col=0)
  df = df[df.columns[df.columns.str.startswith('sol')]]
  df[df==0] = None
  df = df[df.count().sort_values().index].copy()
  return df

def check_data_count_dist(sol_df):
  info_file = '../data/gene_info.csv'
  alpha = 0.05
  alpha_perc = int(100 * alpha)
  df = sol_df.copy()
  df2 = pd.read_csv(info_file, usecols=['start','end','gene_sym'],
                    index_col='gene_sym')
  sr = (df2.end - df2.start).groupby(level=0).max()
  df_adj = df.divide(sr[df.index], axis=0)

  fig, axes = plt.subplots(figsize=(12,7), nrows=3, ncols=3)
  axes = axes.flatten()
  x_arr = np.arange(df.shape[1])
  
  ax = axes[0]
  sr = df.count() / len(df)
  ax.plot(x_arr, sr)
  ax.set_ylabel('non-zero ratio')

  ax = axes[1]
  sr2 = df.mean()
  ax.plot(x_arr, sr2)
  ax.set_ylabel('non-zero mean')
  r = np.corrcoef(sr, sr2)[0,1]
  kws = dict(ha='left', va='top')
  ax.text(0.05, 0.95, f'r={r:.3f}', transform=ax.transAxes, **kws)

  ax = axes[2]
  sr2 = df.fillna(0).mean()
  ax.plot(x_arr, sr2)
  ax.set_ylabel('full mean')
  r = np.corrcoef(sr, sr2)[0,1]
  ax.text(0.05, 0.95, f'r={r:.3f}', transform=ax.transAxes, **kws)

  ax = axes[3]
  sr2 = pd.Series(stats.trim_mean(df.fillna(0), alpha))
  ax.plot(x_arr, sr2)
  ax.set_ylabel('trim mean {alpha_perc}%')
  r = np.corrcoef(sr, sr2)[0,1]
  ax.text(0.05, 0.95, f'r={r:.3f}', transform=ax.transAxes, **kws)

  ax = axes[4]
  sr2 = df_adj.mean()
  ax.plot(x_arr, sr2)
  ax.set_ylabel('adj non-zero mean')
  r = np.corrcoef(sr, sr2)[0,1]
  kws = dict(ha='left', va='top')
  ax.text(0.05, 0.95, f'r={r:.3f}', transform=ax.transAxes, **kws)

  ax = axes[5]
  sr2 = df_adj.fillna(0).mean()
  ax.plot(x_arr, sr2)
  ax.set_ylabel('adj full mean')
  r = np.corrcoef(sr, sr2)[0,1]
  ax.text(0.05, 0.95, f'r={r:.3f}', transform=ax.transAxes, **kws)

  ax = axes[6]
  sr2 = pd.Series(stats.trim_mean(df_adj.fillna(0), alpha))
  ax.plot(x_arr, sr2)
  ax.set_ylabel(f'adj trim mean {alpha_perc}%')
  r = np.corrcoef(sr, sr2)[0,1]
  ax.text(0.05, 0.95, f'r={r:.3f}', transform=ax.transAxes, **kws)

  ax = axes[7]
  df_tpm = df / stats.trim_mean(df_adj.fillna(0), alpha)
  sr2 = df_tpm.mean()
  ax.plot(x_arr, sr2)
  ax.set_ylabel('tpm mean')
  r = np.corrcoef(sr, sr2)[0,1]
  ax.text(0.05, 0.95, f'r={r:.3f}', transform=ax.transAxes, **kws)

  ax = axes[8]
  sr2 = df_tpm.quantile(0.95)
  ax.plot(x_arr, sr2)
  ax.set_ylabel('tpm 95%')
  r = np.corrcoef(sr, sr2)[0,1]
  ax.text(0.05, 0.95, f'r={r:.3f}', transform=ax.transAxes, **kws)
  
  for ax in axes:
    ax.tick_params(length=5)
    ax.set_xlabel(None)
  
  fig.tight_layout(h_pad=0.1)
  fig.show()
  fig.savefig('tmp.png')
  return df_tpm

if __name__ == '__main__':
  if 'sol_df' not in locals():
    sol_df = load_sol_df()
  hoge = check_data_count_dist(sol_df)
