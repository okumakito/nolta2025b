def format_gene_info():
  dir_path = '../data/orig'
  file_list = [x for x in os.listdir(dir_path) if x.startswith('RawCount')]
  file_list.sort()
  out_list = []
  for file_name in file_list[:]:
    file_path = os.path.join(dir_path, file_name)
    print(file_path)
    df = pd.read_table(file_path, usecols=np.arange(9))

    # remove MSTRG
    df = df[~df.GeneID.str.startswith('MSTRG')]
    
    out_list.append(df)

  # merge
  # NOTE: Many EntrezGeneIDs are missing in soleus muscle
  df = pd.concat(out_list, axis=0).sort_values(['GeneID','EntrezGeneID'])
  df = df.drop_duplicates('GeneID')

  # save to file
  df.to_csv('tmp.csv', index=False, float_format='%d')
  return df

if __name__ == '__main__':
  hoge = format_gene_info()
