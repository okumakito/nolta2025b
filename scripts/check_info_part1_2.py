def check_info_part1_2():
  file_name1 = '../data/info_part1_fmt.csv'
  file_name2 = '../data/info_part2_fmt.csv'
  sr1 = pd.read_csv(file_name1, usecols=['bw_2023-02-13']).squeeze()
  sr2 = pd.read_csv(file_name2, usecols=['start_bw']).squeeze()

  print(f'habituation: n={sr1.size}, min={sr1.min()}, max={sr1.max()}')
  print(f'experiment:  n={sr2.size}, min={sr2.min():.2f}, max={sr2.max()}')

  dev_sr = (sr1 - sr1.mean()).abs()
  th = dev_sr.sort_values().iat[-14]
  sr3 = sr1[dev_sr < th]
  print(f'recalculated: n={sr3.size}, min={sr3.min():.2f}, max={sr3.max()}')
  print('allclose:', np.allclose(sr2.sort_values(), sr3.sort_values()))

  return sr1, sr2

if __name__ == '__main__':
  hoge, hoge2 = check_info_part1_2()
