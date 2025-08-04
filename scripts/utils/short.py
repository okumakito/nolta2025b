import numpy as np
import pandas as pd

def mad(df):
  return df.subtract(df.median(axis=1), axis=0).abs().median(axis=1)

def z_score(df):
  return ((df.T - df.T.mean()) / df.T.std()).T
