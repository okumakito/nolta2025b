import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import sys, os, re
import networkx as nx
from scipy import stats
from scipy.cluster.hierarchy import linkage, fcluster, leaves_list, distance
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import utils

sns.set_context('talk', font_scale=0.8)

def load_info():
  file_name = '../data/info.csv'
  return pd.read_csv(file_name)

def load_data_count():
  file_name = '../data/data_count.csv'
  return pd.read_csv(file_name, index_col=0)

def load_data_count_iwat():
  file_name = '../data/data_count_iwat.csv'
  return pd.read_csv(file_name, index_col=0).apply(np.log1p)

def load_sample_info():
  file_name = '../data/sample_info.csv'
  return pd.read_csv(file_name)
