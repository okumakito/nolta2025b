# NOTE: use data_norm_adj_noremove.csv
def check_circadian(data_df):
  gene_list = ['Arntl','Per1']
  df = data_df.loc[gene_list].T.copy()
  df = df.groupby(axis=0,level=0).apply(lambda x:utils.z_score(x.T).T)
  df = df.groupby(axis=0,level=[0,1]).apply(lambda x:x.reset_index(drop=True))
  df.index = df.index.droplevel(1)
  df.index.names = ['organ','sample_no']
  df = df.reset_index()
  df['sample_no'] += 1
  df = df.melt(id_vars=['organ','sample_no'], value_vars=gene_list,
               var_name='gene')
  fig, axes = plt.subplots(figsize=(9,7), nrows=3, ncols=5)
  axes = axes.flatten()
  for ax, (organ, sub_df) in zip(axes, df.groupby('organ')):
    sns.pointplot(data=sub_df, x='sample_no', y='value', hue='gene', ax=ax)
    ax.tick_params(length=5)
    ax.set_title(organ, fontsize=16, pad=10)
    ax.set_xlabel('sample no.')
    ax.set_ylabel(None)
    ax.legend_.remove()
    ax.set_ylim((-2,2))
  for ax in axes[13:]:
    ax.axis('off')
  for i in [0,5,10]:
    axes[i].set_ylabel('z-score')
  fig.tight_layout(h_pad=0.5, w_pad=0.5)
  axes[12].legend(frameon=False, bbox_to_anchor=(1,0.5), borderaxespad=2,
                  handletextpad=0, loc='center left')
  fig.show()
  fig.savefig('tmp.png')
  return df

if __name__ == '__main__':
  hoge = check_circadian(data_df)
