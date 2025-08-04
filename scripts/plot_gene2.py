def plot_gene2(data_df, gene):
  df = data_df.loc[gene].reset_index()
  organ_list =['ewat','iwat','bat','liver','gut','panc','sol','gas',
               'neo','hipp','olf','hypo','pit']
  fig, ax = plt.subplots(figsize=(9,5))
  sns.pointplot(data=df, x='time', y=gene, hue='organ', ax=ax,
                scale=0.8, errwidth=3, ci=None, palette='tab20',
                hue_order=organ_list)
  ax.tick_params(length=5)
  ax.set_ylabel('log expression')
  ax.set_title(gene, fontsize=16, pad=10)
  ax.legend(bbox_to_anchor=(1,1), frameon=False, borderaxespad=0,
            handletextpad=0)
  fig.tight_layout()
  fig.show()
  return df

if __name__ == '__main__':
  gene = sys.argv[1]
  hoge = plot_gene2(data_df, gene)
