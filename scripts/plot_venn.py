import matplotlib_venn as venn
def plot_venn():
  file_name1 = '../data/deg/deg_summary_gene.csv'
  file_name2 = '../data/deg_organ/deg_organ_summary_gene.csv'
  file_name3 = '../data/sfg/sfg_summary_gene.csv'
  sr1 = pd.read_csv(file_name1, usecols=['gene']).squeeze()
  sr2 = pd.read_csv(file_name2, usecols=['gene']).squeeze()
  sr3 = pd.read_csv(file_name3, usecols=['gene']).squeeze()
  area1  = sr1.unique().shape[0]
  area2  = sr2.unique().shape[0]
  area3  = sr3.unique().shape[0]

  fig, ax = plt.subplots(figsize=(6,4))

  # step 1: faces
  patches = venn.venn3_circles([set(sr1), set(sr2), set(sr3)], ax=ax)
  for i, patch in enumerate(patches):
    patch.set_color(plt.cm.tab10(i))
    patch.set_alpha(0.2)

  # step 2: edges (overlay)
  patches2 = venn.venn3_circles([set(sr1), set(sr2), set(sr3)], ax=ax)
  for i, patch in enumerate(patches2):
    patch.set_ec(plt.cm.tab10(i))

  # step 3: labels
  venn.venn3([set(sr1), set(sr2), set(sr3)], ax=ax, alpha=0,
             set_labels=None)
  kws = dict(ha='center', va='center')
  ax.text(-0.8, 0.4, f'DEGs\n(time-varing)\n{area1}', **kws)
  ax.text(0.9, 0.4, f'DEGs\n(organ-specific)\n{area2}', **kws)
  ax.text(-0.1, -0.7, f'SFGs\n{area3}', **kws)

  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return patches[0]

if __name__ == '__main__':
  hoge = plot_venn()
