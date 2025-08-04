def plot_enrichment_nolta(organ):
  file_name = '../data/sfg/sfg_summary_go.csv'
  df = pd.read_csv(file_name)
  df = df[df.group == organ + '_c1']

  fig, axes = plt.subplots(figsize=(12,4), ncols=5, nrows=2)
  axes = axes.flatten()

  for (i, sub_df), ax in zip(df.iterrows(), axes):
    x  = sub_df.overlap
    n1 = sub_df.n_input
    title = sub_df.description
    nt = len(title)
    if nt > 25:
      sr = pd.Series(title.split(' '))
      idx = (((sr.str.len()+1).cumsum() - 1) - nt/2).abs()[::-1].idxmin()
      title = ' '.join(sr[:idx+1]) + '\n' + ' '.join(sr[idx+1:])
    ax.pie([x, n1-x], colors=[plt.cm.Paired(i) for i in [1,0]],
           startangle=90, counterclock=False)
    ax.add_artist(plt.Circle((0,0), 0.6, fc='w'))
    ax.text(0, 0, f'{100*x/n1:.1f}%', ha='center', va='center', fontsize=12)
    ax.text(0, -1.2, title, ha='center', va='top', fontsize=12)

  axes[0].text(-1.2, 1.3, 'D', fontsize=20, ha='right', va='top')
  for i in range(len(df), 10):
    axes[i].axis('off')
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return df

if __name__ == '__main__':
  organ = sys.argv[1]
  hoge = plot_enrichment_nolta(organ)
