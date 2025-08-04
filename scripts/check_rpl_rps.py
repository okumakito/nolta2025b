def check_rpl_rps(iwat_df):
  idx = iwat_df.index
  rp_idx = idx[(idx.str.startswith('Rpl') | idx.str.startswith('Rps'))
               & ~idx.str.startswith('Rps6k')]
  rp_df = iwat_df.loc[rp_idx]
  sr = rp_df.mean()

  fig, axes = plt.subplots(figsize=(10,6), nrows=2, ncols=2,
                           gridspec_kw=dict(height_ratios=[1,0.5]))
  axes = axes.flatten()

  ax = axes[0]
  sns.heatmap(rp_df, cmap='viridis', ax=ax, yticklabels=5,
               xticklabels=False, cbar=False)
  ax.set_xlabel(None)
  ax.set_ylabel(None)
  ax.tick_params(length=0)

  ax = axes[1]
  sns.heatmap(iwat_df.iloc[13500:14000], cmap='viridis', ax=ax,
              yticklabels=False, xticklabels=False, cbar=False)
  ax.set_xlabel(None)
  ax.set_ylabel(None)
  ax.tick_params(length=0)

  ax = axes[2]
  ax.plot(sr.values)
  ax.tick_params(length=5)

  ax = axes[3]
  ax.plot((iwat_df==0).mean().values)
  ax.tick_params(length=5)

  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  if 'iwat_df' not in locals():
    iwat_df = load_data_count_iwat()
  check_rpl_rps(iwat_df)

