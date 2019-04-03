import pandas as pd


schools = pd.read_csv('all_public_schools.csv', sep=',')
schools['count'] = 1
schools.groupby(["2017-2018"])['count'].count()

schools = schools.rename(columns={
    'code région': 'region_code',
})

closed_df = pd.pivot_table(schools, values='count', index="region_code", columns="2017-2018", aggfunc='count', fill_value=0)
closed_df['closed_share'] = closed_df['no'] / (closed_df['no'] + closed_df['yes'])
closed_df.reset_index(inplace=True)
closed_df = closed_df[['region_code', 'closed_share']]

regions = pd.read_csv('regions.csv')
regions = regions.merge(closed_df, on='region_code')

regions.to_csv('regions_with_closed_share.csv', sep=',', index=False)

# closed_df.to_csv('region_closed_percentage.csv', sep=',', index=False)

