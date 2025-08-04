def plot_info(var_name, ylabel):
  df = load_info()
  df = df[~df.condition.str.contains('\+')]
  
  fig, ax = plt.subplots(figsize=(8,4))
  sns.boxplot(data=df, x='condition', y=var_name, ax=ax)
  ax.set_xlabel(None)
  ax.set_ylabel(ylabel)
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
  plot_info(var_name, ylabel)
