import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from .short import mad

def clustering(df, phi):
  Z = linkage(df, metric='correlation', method='average')
  label_arr = fcluster(Z, 1-phi, criterion='distance')
  freq_sr = pd.Series(label_arr).value_counts()
  return label_arr, freq_sr

def calculate_sfg(df_expr, df_ctrl=None, theta=2, phi=None, phi_scale=3,
                  max_clust_num=3, min_clust_size=10, robust=True):
  """
  This function calculates synchronously fluctuated genes (SFGs)
  between two DataFrames.

  Parameters
  ----------
  df_expr :  DataFrame
    Experimental gene expression data (row: genes, col: samples).
  df_ctrl :  DataFrame, optional
    Control gene expression data (row: genes, col: samples).
    Default is None.
  theta : float, optional
    Fold-change cutoff. Default is 2.
  phi : float, optional
    Correlation cutoff. Default is None (auto-adjustment).
  max_clust_num : int, optional
    Maximum cluster number. Default is 3.
  min_clust_size : int, optional
    Minimum cluster size. Default is 10.
  robust : bool, optional
    Useage of robust statistics. Default is True.

  Return
  ------
  gene_arr : ndarray
    synchronously expressed genes.
  """
  # parameter adjustment
  if phi == None:
    phi = np.tanh(phi_scale/np.sqrt(df_expr.shape[1]-3))

  # step 1: deviation filtering
  if robust:
    dev_expr = mad(df_expr)
    if df_ctrl == None:
      dev_ctrl = mad(df_expr).median()
    else:
      dev_ctrl = mad(df_ctrl)
  else:
    dev_expr = df_expr.std(axis=1)
    if df_ctrl == None:
      dev_ctrl = df_expr.std(axis=1).mean()
    else:
      dev_ctrl = df_ctrl.std(axis=1)
  sub_idx = df_expr.index[dev_expr > theta * dev_ctrl]
  if len(sub_idx) < 2: # 0 or 1
    return np.array([])

  # step 2: clustering
  df_sub = df_expr.loc[sub_idx]
  if robust:
    df_sub = df_sub.rank(axis=1)
  label_arr, freq_sr = clustering(df_sub, phi)
  th = 0.5 * freq_sr.iat[0]
  freq_sr = freq_sr.iloc[:max_clust_num]
  freq_sr = freq_sr[freq_sr >= min_clust_size]
  sub_idx = sub_idx[np.isin(label_arr, freq_sr.index[freq_sr > th])]
  return sub_idx.values
