def label_wrap(sr):
  out_list = []
  for x in sr:
    if len(x) >= 6:
      i = int(np.ceil(len(x)/2))
      m = re.match('[^\d]+', x)
      if m:
        i2 = m.end()
        if np.abs(i-i2) <= 2:
          i = i2
      x = x[:i] + '\n' + x[i:]
    out_list.append(x)
  return pd.Series(out_list)

def plot_string2_nolta(file_name, file_postfix=None):

  # load a tsv file obtained from STRING (https://string-db.org/).
  df = pd.read_table(file_name, usecols=[0,1])

  # convert it to a 'Graph' object of networkx
  df.columns = ['source','target']
  df['source'] = label_wrap(df.source)
  df['target'] = label_wrap(df.target)
  G = nx.from_pandas_edgelist(df)

  # select the largest connected component
  lcc_node_set = max(nx.connected_components(G), key=len)
  G = G.subgraph(lcc_node_set)

  # calculate a uniform layout
  pos = utils.uniform_layout(G, seed=12345, circle=True)

  # calculate node colors based on communicability
  # NOTE: nx.communicability() is too slow and not recommended.
  A = nx.adjacency_matrix(G).toarray()
  w_arr, V = np.linalg.eigh(A)
  C = V.dot(np.diag(np.exp(w_arr))).dot(V.T)
  D = 1 / C[np.triu_indices_from(C,1)]
  Z = linkage(D, method='ward', metric='euclidean')
  node_arr = np.asarray(G.nodes())
  sr = pd.Series(np.arange(len(G)), index=node_arr[leaves_list(Z)])
  node_color = sr.loc[node_arr]
  cmap = sns.color_palette('husl', len(G))
  cmap = np.array(cmap) ** 0.5  # brighter
  cmap = mpl.colors.ListedColormap(cmap)

  # calculate node size based on degrees
  scale = 0.2
  degrees = G.degree()
  deg_arr = np.array([degrees[x] for x in G.nodes()])
  deg_arr = 2 * scale * (deg_arr - deg_arr.min()) / \
    (deg_arr.max() - deg_arr.min()) + 1 - scale

  # plot
  n = len(G)
  print(n)
  fig, ax = plt.subplots(figsize=(8,8))
  nx.draw_networkx(G,
                   pos=pos,
                   ax=ax,
                   node_size = np.min([150000 / n, 3000]) * deg_arr,
                   node_color = node_color,
                   cmap = cmap,
                   edge_color = '0.6',
                   width=1,
                   with_labels=False)
  for label, (x,y) in pos.items():
    ax.text(x, y, label, fontsize = np.min([140 / n**0.5, 20]),
            style='italic', ha='center', va='center')
  if n >= 50:
    ax.margins(0)
  else:
    ax.margins(0.05)
  ax.axis('off')
  ax.text(0.02, 0.98, 'C', fontsize=20, transform=ax.transAxes,
          ha='left', va='top')
  fig.tight_layout()
  fig.show()
  if file_postfix is None:
    fig.savefig('tmp.png')
  else:
    fig.savefig(f'tmp_{file_postfix}.png')
  return G

if __name__ == '__main__':
  file_name = sys.argv[1]
  hoge = plot_string2_nolta(file_name)
