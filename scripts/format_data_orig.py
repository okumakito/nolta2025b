def format_data_orig():
  dir_path = '../data/orig'
  info_file = '../data/gene_info.csv'
  file_list = [x for x in os.listdir(dir_path) if x.startswith('RawCount')]
  file_list.sort()
  sr = pd.read_csv(info_file, usecols=['GeneID','EntrezGeneID'],
                   index_col=0).squeeze().dropna()
  out_list = []
  for file_name in file_list[:]:
    file_path = os.path.join(dir_path, file_name)
    print(file_path)
    df = pd.read_table(file_path)

    # select genes with entrez gene id
    df = df[df.GeneID.isin(sr.index)]

    # select protein-coding genes
    df = df[df.gene_biotype=='protein_coding']

    # remove genes with chrJH***, chrGL***
    df = df[df.chr.str.len() <= 5]

    # set gene symbol to index
    df = pd.concat([df.gene_sym, df.iloc[:,15:]], axis=1)
    df = df.set_index('gene_sym').groupby(axis=0,level=0).max()

    # remove all-zero rows
    df = df[df.sum(axis=1)>0]

    # rename columns
    df2 = df.columns.str.split('_', expand=True).to_frame()
    df2[0] = df2[0].replace(dict(hy='hypo', hip='hipp', ob='olf',
                                 nc='neo', pc='panc', si='gut'))
    df.columns = df2[0] + '_' + df2[2] + '_' + df2[1].str[-1]

    # sort time
    sr_day = df2[2].str[:-1].astype(int)
    sr_day[df2[2].str[-1]=='w'] *= 7
    df.columns = [df.columns, sr_day.values]
    df = df.sort_index(axis=1, level=1)
    df.columns = df.columns.droplevel(1)

    out_list.append(df)

  # merge
  df = pd.concat(out_list, axis=1).fillna(0).astype(int)
  df = df.sort_index(axis=0)

  # save to file
  df.index.name = 'gene_symbol'
  df.to_csv('tmp.csv')
  return df

if __name__ == '__main__':
  hoge = format_data_orig()
