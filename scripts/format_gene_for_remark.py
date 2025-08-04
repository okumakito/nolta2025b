def format_gene_for_remark(file_name):
  df = pd.read_csv(file_name)
  for organ, sub_df in df.groupby('organ'):
    out_list = []
    for clust_no, sub2_df in sub_df.groupby('clust_no'):
      sr = sub2_df.head(10).gene
      sr.name = organ + '_c' + str(clust_no)
      sr.index = np.arange(sr.size)+1
      out_list.append(sr)
    df_out = pd.concat(out_list, axis=1)
    df_out.index.name = 'rank'
    df_out.to_csv(f'tmp_{organ}.csv')

if __name__ == '__main__':
  file_name = sys.argv[1]
  format_gene_for_remark(file_name)
