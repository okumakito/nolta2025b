def format_sample_info():
  file_name = '../data/sample_info.xlsx'
  sheet_dict = pd.read_excel(file_name, sheet_name=None)
  out_list = []
  for df in sheet_dict.values():
    out_list.append(df.iloc[:,:9])
  df = pd.concat(out_list, axis=0)
  df.to_csv('tmp.csv', index=False)

if __name__ == '__main__':
  format_sample_info()
