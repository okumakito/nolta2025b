def calc_deg_organ(data_df):
  df = data_df.copy()
  df.columns = df.columns.droplevel(1)

  if False:
    rep_dict=dict(bat='adipo', ewat='adipo', iwat='adipo',
                  sol='muscle', gas='muscle', neo='brain',
                  hipp='brain', hypo='brain', olf='brain')
    df.columns = df.columns.to_series().replace(rep_dict)

  df = df.groupby(axis=1, level=0).mean()
  out_list = []
  for organ in df.columns:
    if False:
      sr = df[organ] - df.drop(organ, axis=1).mean(axis=1)
      sr = sr[sr > 5].sort_values(ascending=False).round(4)
      sr = sr[sr.index.isin(df[df[organ]>20].index)]
    else:
      sr = df[organ]
      sr = sr[sr > sr.quantile(0.9)]
      sr -= df.drop(organ, axis=1).mean(axis=1)
      sr = sr.sort_values(ascending=False).round(4).head(100)
    sr.name = 'mean_diff'
    df_tmp = sr.reset_index()
    df_tmp.insert(0, 'organ', organ)
    out_list.append(df_tmp)
  df = pd.concat(out_list, axis=0)
  df.columns = df.columns.str.replace('gene_symbol','gene')
  df.to_csv('tmp.csv', index=False)
  print(df.organ.value_counts())
  return df

if __name__ == '__main__':
  res_df = calc_deg_organ(data_df)
