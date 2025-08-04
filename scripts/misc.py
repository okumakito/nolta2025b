def check_sol_atp5(data_df):
  df = data_df.groupby(axis=1, level=0).mean()
  fig, ax = plt.subplots(figsize=(8,8))
  sns.heatmap(df.iloc[1660:1690], cmap='viridis', ax=ax, yticklabels=1)
  ax.tick_params(length=0)
  ax.set_xlabel(None)
  ax.set_ylabel(None)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

def format_david_demo(n):
  file_name = f'../data/david_demo/demo{n}_gene_orig.tsv'
  sr = pd.read_table(file_name, usecols=['Name']).squeeze()
  sr = sr[sr.str.contains('\(')]
  sr = sr.str.rsplit('(',1).str[1].str[:-1].sort_values().drop_duplicates()
  sr.to_csv('tmp.csv', index=False, header=False)
  return sr

def parse_deg_organ():
  file_name = '../data/deg_organ/deg_organ_summary_gene.csv'
  sr = pd.read_csv(file_name).set_index('organ').gene_symbol
  for organ, sr2 in sr.groupby(level=0):
    sr2.sort_values().to_csv(f'tmp_{organ}.csv', index=False, header=False)

def plot_string_batch():
  dir_path = '../data/deg_organ/'
  #dir_path = '../data/deg/'
  #dir_path = '../data/sfg/'
  file_list = os.listdir(dir_path)
  file_list = [x for x in file_list if '_nw.tsv' in x]
  file_list.sort()
  for file_name in file_list:
    file_path = os.path.join(dir_path, file_name)
    print(file_path)

    organ = file_name.split('_')[0]
    title = f'{organ}-specific DEGs'
    file_postfix = organ

    #file_postfix = file_name.rsplit('_',1)[0]
    #clust = file_postfix.replace('_','-')
    #title = f'{clust} DEGs'
    #title = f'{clust} SFGs'
    print(file_path, title, file_postfix)

    plot_string2(file_path, title, file_postfix)
    plt.close('all')

def gen_data_mean(data_df):
  df = data_df.groupby(axis=1,level=[0,1],sort=False).mean().round(4)
  df.columns = df.columns.get_level_values(0) + '_' + \
    df.columns.get_level_values(1)
  df.to_csv('tmp.csv')

# requirement: plot_max_eigval.py > df_max_eigval
def format_peak_summary(df_max_eigval):
  sr = df_max_eigval.idxmax(axis=1)
  df = pd.read_csv('../data/sfg/sfg_summary_gene.csv')
  df['group'] = df.organ + '-c' + df.clust_no.astype(str)
  sr2 = df.groupby('group').count().gene
  df_out = pd.concat([sr, sr2], axis=1)
  df_out.columns = ['peak', 'n_gene']
  df_out = df_out.sort_index()
  df_out.to_csv('tmp.csv')

def check_david_string_mapped():
  dir_path = '../data/sfg'
  file_list = os.listdir(dir_path)
  #file_list = [x for x in file_list if '_go.tsv' in x]
  file_list = [x for x in file_list if '_nw.tsv' in x]
  file_list.sort()
  for file_name in file_list:
    file_path = os.path.join(dir_path, file_name)
    df = pd.read_table(file_path)
    #print(file_name, df['List Total'].iat[0])
    print(file_name, np.union1d(df['#node1'], df['node2']).size)

def check_periodic():
  file_name = '../data/sfg/sfg_summary_gene_nolta.csv'
  clust_list = [('liver',1), ('liver',2), ('pit',1), ('pit',2),
                ('gut',2), ('neo',1)]
  df = pd.read_csv(file_name)
  out_list = []
  for organ, clust_no in clust_list:
    out_list.append(df[(df.organ==organ) & (df.clust_no==clust_no)].gene)
  sr = pd.Series(np.concatenate(out_list))
  print(sr.value_counts().head(20))

def calc_overlap_gene():
  file_name = '../data/sfg/sfg_summary_gene_nolta.csv'
  df = pd.read_csv(file_name)
  df['label'] = df.organ + '_c' + df.clust_no.astype(str)
  sr = df.set_index('label').gene
  out_list = []
  for label1, sr1 in sr.groupby(level=0):
    for label2, sr2 in sr.groupby(level=0):
      if label1 == label2:
        continue
      df_tmp = pd.DataFrame(np.intersect1d(sr1, sr2), columns=['gene'])
      df_tmp.insert(0, 'clust1', label1)
      df_tmp.insert(1, 'clust2', label2)
      out_list.append(df_tmp)
  df = pd.concat(out_list, axis=0)
  df.to_csv('tmp.csv', index=False)

if __name__ == '__main__':
  #check_sol_atp5(data_df)
  #hoge = format_david_demo(2)
  #parse_deg_organ()
  #plot_string_batch()
  #gen_data_mean(data_df)
  #format_peak_summary(df_max_eigval)
  #check_david_string_mapped()
  #check_periodic()
  calc_overlap_gene()
