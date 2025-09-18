def check_table2_nolta():
  file_name1 = '../data/sfg/sfg_summary_gene_nolta.csv'
  file_name2 = '../data/sfg/sfg_summary_lcc.csv'
  df1 = pd.read_csv(file_name1)
  df2 = pd.read_csv(file_name2)
  out_list = []
  for (organ, clust_no), sub_df in df1.groupby(['organ','clust_no']):
    sr = df2[(df2.organ==organ) & (df2.clust_no==clust_no)].gene
    sub_df['in_lcc'] = sub_df.gene.isin(sr).astype(int)
    out_list.append(sub_df)
  df = pd.concat(out_list, axis=0)
  df.to_csv('tmp.csv', index=False)
  return df

if __name__ == '__main__':
  hoge = check_table2_nolta()
