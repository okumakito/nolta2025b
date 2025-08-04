def format_go_for_remark(file_name):
  df = pd.read_csv(file_name)
  for group, sub_df in df.groupby('group'):
    df_tmp = sub_df[['group','description','overlap']].head(10).copy()
    df_tmp.columns = ['cluster','GO term','overlap']
    #df_tmp.columns = ['organ','GO term','overlap']
    df_tmp.to_csv(f'tmp_{group}.csv', index=False)

if __name__ == '__main__':
  file_name = sys.argv[1]
  format_go_for_remark(file_name)
