def enrichment(dir_path):
  min_ratio = 0.05
  min_count = 5
  fdr = 0.05
  postfix = '_go.tsv'
  file_list = [x for x in os.listdir(dir_path) if x.endswith(postfix)]
  file_list.sort()
  out_list = []
  for file_name in file_list[:]:
    file_path = os.path.join(dir_path, file_name)
    df = pd.read_table(file_path, usecols=['Term','Count','List Total',
                                           'Pop Hits','Pop Total'])
    if len(df) == 0:
      continue
    df.columns = ['term','overlap','n_input','n_target','n_total']
    df = df[df.overlap >= df.n_input * min_ratio]
    df = df[df.overlap >= min_count]
    df = df[~df.term.str.contains('regulation of transcription')]
    if len(df) == 0:
      continue
    df['p_val'] = stats.hypergeom.sf(df.overlap-1, df.n_total,
                                     df.n_input, df.n_target)
    df['q_val'] = utils.calculate_q(df.p_val)
    df = df[df.q_val < fdr]
    if len(df) == 0:
      continue
    df.insert(1,'description', df.term.str.split('~').str[1])
    df['term'] = df.term.str.split('~').str[0]
    df.insert(0, 'group', file_name.replace(postfix,''))
    df = df.sort_values(['overlap','p_val'], ascending=[False,True])
    out_list.append(df)
  df = pd.concat(out_list, axis=0)
  df.to_csv('tmp.csv', index=False, float_format='%.2e')
  return df

if __name__ == '__main__':
  dir_path = sys.argv[1] # ../data/deg_smd
  hoge = enrichment(dir_path)
