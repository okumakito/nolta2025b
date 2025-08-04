def format_read_info():
  dir_path = '../data/orig'
  file_list = [x for x in os.listdir(dir_path) if x.startswith('Map_stat')]
  file_list.sort()
  out_list = []
  for file_name in file_list:
    file_path = os.path.join(dir_path, file_name)
    print(file_path)
    df = pd.read_table(file_path)
    out_list.append(df)
  df = pd.concat(out_list, axis=0)
  df.to_csv('tmp.csv', index=False)

if __name__ == '__main__':
  format_read_info()
