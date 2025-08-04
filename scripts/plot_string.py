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

def plot_string(file_name, title):

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

  # calculate node colors based on degrees
  degrees = G.degree()
  node_color = [degrees[x] for x in G.nodes()]
  d_max = max(node_color)

  # output degrees
  sr = pd.Series(dict(degrees)).sort_values(ascending=False)
  sr.index.name = 'gene'
  sr.name = 'degree'
  sr.index = sr.index.str.replace('\n','')
  sr.to_csv('tmp.csv')

  # calculate node size based on degrees
  scale = 0.2
  deg_arr = np.array(node_color)
  deg_arr = 2 * scale * (deg_arr - deg_arr.min()) / \
    (deg_arr.max() - deg_arr.min()) + 1 - scale

  # plot
  n = len(G)
  fig, ax = plt.subplots(figsize=(8,8))
  nx.draw_networkx(G,
                   pos=pos,
                   ax=ax,
                   node_size = np.min([150000 / n, 3000]) * deg_arr,
                   font_size = np.min([140 / n**0.5, 20]),
                   node_color = node_color,
                   cmap = 'Blues',
                   vmin = -1 * d_max,
                   vmax = 2 * d_max,
                   edge_color = '0.6',
                   width=1)
  ax.margins(np.clip(300 / n**2, 0.05, 0.2),
             np.clip(0.05 + 200 / n**2, 0.05, 0.2))
  ax.axis('off')
  ax.text(0.02, 0.98, title, fontsize=16, transform=ax.transAxes,
          ha='left', va='top')
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  return G

if __name__ == '__main__':
  file_name = sys.argv[1]
  title = sys.argv[2]
  hoge = plot_string(file_name, title)
