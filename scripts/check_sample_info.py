def check_sample_info():
  df = load_sample_info()[['Sample Name','Total amount(ug)','RIN']]
  df.columns = ['sample_name','total_amount','RIN']
  df['organ'] = df.sample_name.str.split('_').str[0]
  df = df.groupby('organ').apply(lambda x:x.reset_index(drop=True))
  df = df.unstack().RIN
  #df = df.unstack().total_amount
  replace_dict = dict(hip='hipp', hy='hypo', nc='neo', ob='olf', pc='panc',
                      si='gut')
  df.index = df.index.to_series().replace(replace_dict)
  df = df.sort_index(axis=0)

  fig, ax = plt.subplots(figsize=(6,4))
  g = sns.heatmap(df, cmap='Blues', ax=ax)
  g.set_facecolor('0.8')
  ax.tick_params(length=0)
  ax.set_xlabel('samples')
  ax.set_ylabel(None)
  ax.set_title('RIN', fontsize=16, pad=10)
  #ax.set_title('Total amount (ug)', fontsize=16, pad=10)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
  cb = ax.collections[0].colorbar
  cb.outline.set_linewidth(1)
  cb.ax.tick_params(length=2, width=1)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df

if __name__ == '__main__':
  hoge = check_sample_info()
