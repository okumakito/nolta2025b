def plot_string_for_qiita(file_name):

  # load a tsv file obtained from STRING (https://string-db.org/).
  df = pd.read_table(file_name, usecols=[0,1])

  # convert it to a 'Graph' object of networkx
  df.columns = ['source','target']
  G = nx.from_pandas_edgelist(df)

  # select the largest connected component
  lcc_node_set = max(nx.connected_components(G), key=len)
  G = G.subgraph(lcc_node_set)

  # calculate a uniform layout
  pos = utils.uniform_layout(G, seed=12345, circle=True)

  # calculate node colors based on degrees
  degrees = G.degree()
  nodes = G.nodes()
  node_color = [degrees[x] for x in nodes]
  d_max = max(node_color)

  # plot
  n = len(G)
  fig, ax = plt.subplots(figsize=(8,8))
  nx.draw_networkx(G,
                   pos=pos,
                   ax=ax,
                   node_size = np.min([10**5 / n, 5000]),
                   font_size = np.min([120 / n**0.5, 20]),
                   nodelist = nodes,
                   node_color = node_color,
                   cmap = 'Blues',
                   vmin = -1 * d_max,
                   vmax = 2 * d_max,
                   edge_color = '0.7',
                   width=1)
  if n > 50:
    ax.margins(0.1,0.05)
  elif n > 30:
    ax.margins(0.15,0.1)
  else:
    ax.margins(0.2)
  ax.axis('off')
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  file_name = sys.argv[1]
  plot_string_for_qiita(file_name)
