def format_sfg_list(data_df):
  dir_path = '../data/sfg/'
  file_list = os.listdir(dir_path)
  file_list = [x for x in file_list if re.search('_c\d_gene', x)]
  out_list = []
  for file_name in file_list:
    file_path = os.path.join(dir_path, file_name)
    organ = file_name.split('_')[0]
    clust_no = file_name.split('_')[1][-1]
    sr = pd.read_csv(file_path, header=None).squeeze()
    df = data_df.loc[sr, organ]

    # imura score
    #w_arr, v_arr = np.linalg.eigh(utils.z_score(df).T.cov())
    df2 = df.groupby(axis=1,level=0,sort=False).\
      apply(lambda x:(x.T-x.T.mean()).T)
    w_arr, v_arr = np.linalg.eigh(df2.T.cov())
    df_tmp = sr.to_frame('gene')
    w = w_arr[-1]
    v = np.abs(v_arr[:,-1])
    v/= v.max()
    df_tmp['score'] = w * v

    df_tmp.insert(0, 'organ', organ)
    df_tmp.insert(1, 'clust_no', clust_no)
    out_list.append(df_tmp)
  df = pd.concat(out_list, axis=0)
  df = df.sort_values(['organ','clust_no','score'],
                      ascending=[True, True, False])
  df['score'] = df.score.round(3)
  df.to_csv('tmp.csv', index=False)
  return df

if __name__ == '__main__':
  hoge = format_sfg_list(data_df)
