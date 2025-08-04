def format_info_part2():
  file_name = '../data/info_part2.csv'
  df = pd.read_csv(file_name, header=None)
  out_list = []
  for i in range(int(len(df)/7)):
    sub_df = df.iloc[7*i : 7*(i+1)]
    df2 = sub_df.iloc[1:].copy()
    df2.columns = ['condition','no','start_bw','dissect_bw']
    df2.insert(2, 'start_date', sub_df.iat[0,2])
    df2.insert(3, 'dissect_date', sub_df.iat[0,3])
    out_list.append(df2)
  df = pd.concat(out_list, axis=0)
  df['condition'] = df.condition.ffill()
  df['no'] = df.no.str.replace('No.','', regex=False)
  def format_date(sr):
    df2 = sr.str.extract('(\d+)月(\d+)日')
    return '2023-' + df2[0].str.rjust(2, '0') + '-' + df2[1].str.rjust(2, '0')
  df['start_date'] = format_date(df.start_date)
  df['dissect_date'] = format_date(df.dissect_date)
  sr = pd.to_datetime(df.dissect_date) - pd.to_datetime(df.start_date)
  df.insert(4, 'days_recalc', sr.dt.days -1)
  df.to_csv('tmp.csv', index=False)
  return df

if __name__ == '__main__':
  hoge = format_info_part2()
