def format_info_part2_3_fmt():
  file_name_p2 = '../data/info_part2_fmt.csv'
  file_name_p3 = '../data/info_part3_fmt.csv'
  df = pd.read_csv(file_name_p2)
  df2 = pd.read_csv(file_name_p3)
  df_out = df.merge(df2)
  df_out.to_csv('tmp.csv', index=False)
  return df_out

if __name__ == '__main__':
  hoge = format_info_part2_3_fmt()
