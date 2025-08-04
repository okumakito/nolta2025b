import numpy as np
import networkx as nx
from scipy.cluster.hierarchy import distance

def uniform_layout(G, alpha=0.1, n_iter=None, seed=None, circle=False,
                   **kwargs):
  """
  This function calculates uniformly distributed vertex positions
  for a networkx graph. Initial positions are determined using
  networkx.spring_layout function, and then repelling force
  between vertices is applied.

  Parameters
  ----------
  G : networkx graph
    Input network.
  alpha : float, optional
    Strength of repelling force between 0 and 1.
  n_iter : int, optional
    Number of iterations. If set to None, 10 times the number of
    vertices is used.
  seed : int, optional
    Seed for random numbers.
  circle : bool, optional
    If True, nodes are put within a circle. Otherwise, they are put
    within a square. Default is False.
  kwargs : other keyword arguments
    They are passed to networkx.spring_layout function.

  Returns
  -------
  pos : dict
    Vertex positions.

  Example
  -------
  >>> G = nx.Graph()
  >>> G.add_edges_from([(0,1),(1,2),(2,0),(2,3),(3,4),(4,5),(5,3)])
  >>> pos = uniform_layout(G)
  >>> nx.draw_networkx(G, pos=pos)
  """
  pos = nx.spring_layout(G, seed=seed, **kwargs)
  X = np.array(list(pos.values()))
  if n_iter == None:
    n_iter = 10 * len(G)
  for _ in range(n_iter):
    D = distance.squareform(distance.pdist(X))
    np.fill_diagonal(D, None)
    X += alpha * (X - X[np.nanargmin(D, axis=0)])
    if circle:
      X = (X.T / np.linalg.norm(X,axis=1).clip(1,None)).T
    else:
      X = X.clip(-1,1)
  return dict(zip(pos.keys(), X))
