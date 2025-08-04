sns.set_context('paper', font_scale=1.2)
def plot_info_nolta():
  df = load_info()
  df = df[~df.condition.str.contains('\+')]
  var_list = ['dissect_bw', 'blood_sugar', 'ewat', 'iwat', 'bat',
              'liver', 'soleus', 'gastro']
  ylabel_list = ['body weight (g)', 'blood glucose (mg/dL)',
                 'eWAT weight (mg)', 'iWAT weight (mg)',
                 'BAT weight (mg)', 'liver weight (mg)',
                 'soleus muscle weight (mg)', 'gastro. muscle weight (mg)']
  char_list = list('ABCDEFGH')

  fig, axes = plt.subplots(figsize=(12,12), ncols=2, nrows=4)
  axes = axes.flatten()

  for ax, var, ylabel, char in zip(axes, var_list, ylabel_list, char_list):
    sns.boxplot(data=df, x='condition', y=var, ax=ax, color='w',
                linecolor='C0', showcaps=False,
                flierprops=dict(marker='x'))
    ax.set_xlabel(None)
    ax.set_ylabel(ylabel)
    xticklabels = [x.get_text()[:-1] + '\n' + x.get_text()[-1]
                   for x in ax.get_xticklabels()]
    ax.set_xticks(ax.get_xticks(), xticklabels, linespacing=0.9)
    ax.tick_params(length=5)
    ax.set_xlim((-0.8, ax.get_xlim()[1]+0.3))
    ax.grid(axis='y')
    ax.text(-0.15, 1, char, fontsize=16, transform=ax.transAxes,
            ha='right', va='top')
  fig.tight_layout(h_pad=1, w_pad=2)
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  plot_info_nolta()
