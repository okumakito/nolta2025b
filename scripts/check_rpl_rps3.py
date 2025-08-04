def check_rpl_rps3(iwat_df):
  idx = iwat_df.index
  rp_idx = idx[(idx.str.startswith('Rpl') | idx.str.startswith('Rps'))
               & ~idx.str.startswith('Rps6k')]
  sr = iwat_df.loc[rp_idx].mean()
  sr = (sr - sr.mean()) / sr.std()
  df = utils.z_score(iwat_df)
  corr_sr = (df * sr).mean(axis=1).sort_values(ascending=False)
  corr_sr.name = 'corr'
  corr_sr.round(4).to_csv('tmp.csv')

  fig, ax = plt.subplots(figsize=(6,4))
  ax.plot(corr_sr.values)
  ax.set_xlabel('genes')
  ax.set_ylabel('correlation')
  ax.tick_params(length=5)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return corr_sr

if __name__ == '__main__':
  if 'iwat_df' not in locals():
    iwat_df = load_data_count_iwat()
  hoge = check_rpl_rps3(iwat_df)

