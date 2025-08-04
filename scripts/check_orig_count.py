def check_orig_count():
  dir_path = '../data/orig'
  file_list = [x for x in os.listdir(dir_path) if x.startswith('RawCount')]
  file_list.sort()
  out_list = []
  for file_name in file_list[:]:
    file_path = os.path.join(dir_path, file_name)
    print(file_path)
    df = pd.read_table(file_path)

    # remove MSTRG
    #df = df[~df.GeneID.str.startswith('MSTRG')]
      
    # select genes with entrez gene id
    df = df[~df.EntrezGeneID.isnull()]

    df = df.iloc[:,15:]
    sr1 = df.sum()
    sr2 = (df>0).sum()
    df2 = pd.concat([sr1, sr2], axis=1)
    df2.columns = ['total_count','detected_genes']
    out_list.append(df2)

  # merge
  df = pd.concat(out_list, axis=0)
  df.index.name = 'sample_name'

  df['organ'] = df.index.str.split('_').str[0]
  fig, axes = plt.subplots(figsize=(6,5), nrows=2)
  kws = dict(showfliers=False)
  sns.boxplot(data=df, x='organ', y='total_count', ax=axes[0], **kws)
  sns.boxplot(data=df, x='organ', y='detected_genes', ax=axes[1], **kws)
  for ax in axes:
    ax.tick_params(length=5)
    ax.set_xlabel(None)
    ax.margins(0.1, 0.2)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df

if __name__ == '__main__':
  hoge = check_orig_count()
