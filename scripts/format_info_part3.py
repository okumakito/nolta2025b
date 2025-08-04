def format_info_part3():
  file_name = '../data/info_part3.csv'
  df = pd.read_csv(file_name, header=None)
  out_list = []
  for i in range(int(len(df)/10)):
    sub_df = df.iloc[10*i : 10*(i+1)]
    out_list.append(sub_df.iloc[2:-2])
  df = pd.concat(out_list, axis=0)
  df.columns = ['condition','no','blood_sugar','ewat','iwat','bat',
                'liver','soleus','gastro']
  df['condition'] = df.condition.ffill()
  df['no'] = df.no.str.replace('No.','', regex=False)
  df.to_csv('tmp.csv', index=False)
  return df

if __name__ == '__main__':
  hoge = format_info_part3()
