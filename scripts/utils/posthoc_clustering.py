import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from .short import z_score

def posthoc_clustering(df_in, phi_scale=3, min_clust_size=100):
  df_norm = z_score(df_in)
  Z = linkage(df_norm, metric='correlation', method='average')
  phi = np.tanh(phi_scale/np.sqrt(df_in.shape[1]-3))
  sr = pd.Series(fcluster(Z, 1-phi, criterion='distance'), index=df_in.index)
  freq_sr = sr.value_counts()
  freq_sr = freq_sr[freq_sr >= min_clust_size]
  sr = sr[sr.isin(freq_sr.index)]
  sr = sr.replace(freq_sr.index, np.arange(freq_sr.size)+1)
  df = sr.reset_index()
  df.columns = ['gene','clust']
  df = df[['clust','gene']].sort_values(['clust','gene'])
  return df
