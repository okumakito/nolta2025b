def check_featureCounts():
  file_name1 = '../data/orig_old/RawCount_Matrix_ann_ewat.tsv'
  file_name2 = '../data/orig/RawCount_Matrix_ann_ewat.tsv'
  df1 = pd.read_table(file_name1)
  df2 = pd.read_table(file_name2)
  df1 = df1[~df1.GeneID.str.startswith('MSTRG')]

  print('# emsembl')
  print(df1.GeneID.size, df2.GeneID.size,
        np.intersect1d(df1.GeneID, df2.GeneID).size)

  print('# entrez')
  print(df1.EntrezGeneID.unique().size, df2.EntrezGeneID.unique().size,
        np.intersect1d(df1.EntrezGeneID, df2.EntrezGeneID).size)

  # NOTE: all ensembl ID in file1 are included in file2
  df1 = df1.set_index('GeneID')
  df2 = df2.set_index('GeneID')
  df1 = df1[df1.iloc[:,-96:].mean(axis=1)>100]
  df2 = df2.loc[df1.index]
  df = df2.iloc[:,-96:] - df1.iloc[:,-96:]
  idx = df.sum(axis=1).sort_values(ascending=False).index
  df1.insert(3, 'length', df1.end - df1.start)
  df = pd.concat([df1.iloc[:,:9], df], axis=1).loc[idx]
  df.to_csv('tmp.csv')

  # skew
  sr1 = (df1.iloc[:,-96:]+1).apply(np.log2).skew(axis=1)
  sr2 = (df2.iloc[:,-96:]+1).apply(np.log2).skew(axis=1)
  print(sr1.describe())
  print(sr2.describe())
  sr1.name = 'StringTie'
  sr2.name = 'featureCounts'
  df = pd.concat([sr1, sr2], axis=1)
  fig, ax = plt.subplots(figsize=(4,4))
  sns.boxplot(data=df, ax=ax, showfliers=False)
  ax.tick_params(length=5)
  ax.set_ylabel('skewness')
  ax.set_xlim((-0.6,1.6))
  ax.margins(0.1)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df1

if __name__ == '__main__':
  hoge = check_featureCounts()
