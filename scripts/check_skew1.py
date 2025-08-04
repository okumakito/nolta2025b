def check_skew1(data_df):
  fig, axes = plt.subplots(figsize=(12,10), nrows=4, ncols=4)
  axes = axes.flatten()
  for (organ, sub_df), ax in zip(data_df.groupby(axis=1,level=0), axes):
    df = sub_df[sub_df.mean(axis=1)>5][organ]
    df = df[df.min(axis=1)>0]
    sr = pd.Series(utils.z_score(df).values.ravel())
    sns.distplot(sr, ax=ax, kde=False, norm_hist=True, bins=100)
    ax.tick_params(length=5)
    ax.set_xlim((-3, 3))
    ax.set_ylim((0, 0.8))
    ax.set_title(organ, fontsize=16, pad=10)
    ax.set_xlabel('z score')
    ax.set_ylabel('probability')
    ax.axvline(0, c=plt.cm.tab10(0), lw=1)
    ax.text(0.05, 0.95, f'skewness = {sr.skew():.2f}',
            ha='left', va='top', transform=ax.transAxes)
  for ax in axes[13:]:
    ax.set_axis_off()
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')

if __name__ == '__main__':
  check_skew1(data_df)
