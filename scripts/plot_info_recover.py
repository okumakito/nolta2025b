def plot_info_recover(var_name, ylabel):
  df = load_info()
  t_list = ['1d', '1w', '2w', '4w', '6w', '8w', '10w']
  df = df[df.condition.str.split('\+').str[0].isin(t_list)]

  color_dict = {}
  for t in df.condition.unique():
    color_dict[t] = plt.cm.tab10(t_list.index(t.split('+')[0]))
  
  fig, ax = plt.subplots(figsize=(12,4))
  sns.boxplot(data=df, x='condition', y=var_name, ax=ax,
              palette=color_dict)
  ax.set_xlabel('HFD (+ normal chow)')
  ax.set_ylabel(ylabel)
  ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
  ax.tick_params(length=5)
  ax.set_xlim((-0.8, ax.get_xlim()[1]+0.3))
  ax.grid(axis='y')
  ax.set_axisbelow(True)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  var_name = sys.argv[1]
  ylabel = sys.argv[2]
  hoge = plot_info_recover(var_name, ylabel)
