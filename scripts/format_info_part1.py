def format_info_part1():
  file_name = '../data/info_part1.csv'
  df = pd.read_csv(file_name)
  df.columns = ['cage_no', 'mouse_no',
                'bw_2023-02-07', 'bw_2023-02-10', 'bw_2023-02-13']
  df['cage_no'] = df.cage_no.str.split('No.').str[1].ffill()
  df['mouse_no'] = df.mouse_no.str.replace('No.','', regex=False)
  df.to_csv('tmp.csv', index=False)
  return df

if __name__ == '__main__':
  hoge = format_info_part1()

