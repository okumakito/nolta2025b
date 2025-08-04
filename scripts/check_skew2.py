def check_skew2(data_df):
  out_list = []
  for organ, sub_df in data_df.groupby(axis=1,level=0):
    df = sub_df[sub_df.mean(axis=1)>5][organ]
    df = df[df.min(axis=1)>0]
    sr = utils.z_score(df).skew(axis=1)
    sr.name = organ
    out_list.append(sr)
  df = pd.concat(out_list, axis=1)
  fig, ax = plt.subplots(figsize=(6,4))
  sns.boxplot(data=df, showfliers=False, ax=ax)
  ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
  ax.set_ylabel('skewness per gene')
  ax.set_xlim((-0.8, 12.8))
  ax.tick_params(length=5)
  ax.axhline(0, c=plt.cm.tab10(3), lw=2, ls='--')
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df

if __name__ == '__main__':
  hoge = check_skew2(data_df)
