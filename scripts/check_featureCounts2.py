def check_featureCounts2():
  file_name1 = '../data/orig_old/RawCount_Matrix_ann_ewat.tsv'
  file_name2 = '../data/orig/RawCount_Matrix_ann_ewat.tsv'
  df1 = pd.read_table(file_name1)
  df2 = pd.read_table(file_name2)
  df1 = df1[~df1.GeneID.str.startswith('MSTRG')]
  df1 = df1.set_index('GeneID')
  df2 = df2.set_index('GeneID')
  sr1 = (df1.iloc[:,-96:]+1).apply(np.log2).mean(axis=1)
  sr2 = (df2.iloc[:,-96:]+1).apply(np.log2).mean(axis=1)
  idx = sr1[sr1 > 0].index.intersection(sr2[sr2 > 0].index)
  sr1 = sr1.loc[idx]
  sr2 = sr2.loc[idx]

  fig, ax = plt.subplots(figsize=(6,6))
  ax.scatter(sr1, sr2, s=1)
  ax.tick_params(length=5)
  ax.set_xlabel('StringTie')
  ax.set_ylabel('featureCounts')
  ax.plot([0,20],[0,20], c=plt.cm.tab10(3))
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df1

if __name__ == '__main__':
  hoge = check_featureCounts2()
