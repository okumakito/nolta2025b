import numpy as np

def calculate_q(p_seq):
  """
  This function calculates q-values from p-values
  by using Benjamini-Hochberg method.

  Parameters
  ----------
  p_seq : array-like
    p-values

  Returns
  -------
  q_arr : ndarray
    q-values
  """
  p_arr   = np.asarray(p_seq)
  N       = len(p_arr)
  idx_arr = np.argsort(p_arr)
  q_arr   = p_arr[idx_arr] * N / (np.arange(N) + 1)
  q_arr   = np.minimum.accumulate(q_arr[::-1])[::-1]
  q_arr[idx_arr] = q_arr.copy()
  return q_arr

if __name__ == '__main__':
  p_arr = np.random.rand(5)**2
  q_arr = calculate_q(p_arr)
  print('p-values', p_arr)
  print('q-values', q_arr)
