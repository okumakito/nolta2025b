def format_data_count():
  data_file = '../data/data_count.csv'
  info_file = '../data/gene_info.csv'
  df = pd.read_csv(data_file, index_col=0)
  df2 = pd.read_csv(info_file, usecols=['start','end','gene_sym'],
                    index_col='gene_sym')
  sr = (df2.end - df2.start).groupby(level=0).max()

  if False:
    ribosome_file = '../data/ribosome_corr.csv'
    sr2 = pd.read_csv(ribosome_file, index_col=0).squeeze()
    df = df.drop(sr2[sr2>0.5].index, axis=0)
    print(df.shape)

  # modified TPM using trimemd mean
  alpha = 0.05
  df = df.divide(sr[df.index], axis=0)
  if True:
    df = df / stats.trim_mean(df, alpha) / len(df)
  else:
    df3 = df.copy()
    df3[df3==0] = None
    df3[(df3 > df3.quantile(1-alpha)) | (df3 < df3.quantile(alpha))] = None
    df = df / df3.mean() / len(df)
  df *= 10**6

  # log2
  df = df.apply(np.log2)
  df[df==-np.inf] = None
  df -= df.min().min()
  df = df.fillna(0)
  
  # round
  df = df.round(4)

  # save to file
  df.to_csv('tmp.csv')
  return df

if __name__ == '__main__':
  hoge = format_data_count()
