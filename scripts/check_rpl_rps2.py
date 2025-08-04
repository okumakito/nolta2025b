def check_rpl_rps2(iwat_df):
  idx = iwat_df.index
  rp_idx = idx[(idx.str.startswith('Rpl') | idx.str.startswith('Rps'))
               & ~idx.str.startswith('Rps6k')]
  rp_df = iwat_df.loc[rp_idx]
  sr = rp_df.mean()

  fig, axes = plt.subplots(figsize=(12,8), nrows=2, ncols=3)
  axes = axes.flatten()

  def func(sr2, ylabel, ax):
    ax.scatter(sr, sr2, s=5)
    ax.set_xlabel('Rpl/Rps genes')
    ax.set_ylabel(ylabel)
    ax.tick_params(length=5)
    ax.margins(0.1, 0.2)
    r = np.corrcoef(sr, sr2)[0,1]
    ax.text(0.05, 0.05, f'r={r:.3f}', transform=ax.transAxes,
            ha='left', va='bottom')

  func(iwat_df.mean(), 'mean expression', axes[0])
  func((iwat_df==0).mean(), 'zero ratio', axes[1])
  func(iwat_df[iwat_df!=0].mean(), 'non-zero mean expression', axes[2])
  func((np.exp(iwat_df)-1).sum(), 'total count', axes[3])
  
  mt_idx = idx[idx.str.startswith('mt')]
  func(iwat_df.loc[mt_idx].mean(), 'mitochondria genes', axes[4])

  mrp_idx = idx[idx.str.startswith('Mrp')]
  func(iwat_df.loc[mrp_idx].mean(), 'Mrpl/Mrps genes', axes[5])
  
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  if 'iwat_df' not in locals():
    iwat_df = load_data_count_iwat()
  check_rpl_rps2(iwat_df)

