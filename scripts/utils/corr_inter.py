import numpy as np

def corr_inter(X, Y):
  """
  This is a python implementation of Matlab's corr(X,Y), which "returns a 
  matrix of the pairwise correlation coefficient between each pair of 
  columns in the input matrices X and Y" (cited from the Matlab's official 
  documentation). In contrast to np.corrcoef(X,Y,rowvar=0), this function 
  evaluates only the column pairs belonging to different input matrices.
   
  Parameters
  ----------
  X : ndarray (n x p1)
  Y : ndarray (n x p2)
  
  Return
  ------
  R : ndarray (p1 x p2)
    matrix of the pairwise corelation coefficient
  """
  X_normed = (X - X.mean(axis=0)) / X.std(axis=0, ddof=0)
  Y_normed = (Y - Y.mean(axis=0)) / Y.std(axis=0, ddof=0)
  return np.dot(X_normed.T, Y_normed) / X.shape[0]
