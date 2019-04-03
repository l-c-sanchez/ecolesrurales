import pandas as pd

# positions = pd.read_csv('ecole-gps.csv', sep=';')
# regions = pd.read_csv('ecole_regions.csv', sep=';')

positions = pd.read_csv('ecole-gps.csv', sep='\t')
regions = pd.read_csv('ecole_regions.csv', sep='\t')

positions = positions.iloc[:, 0:3]
positions.columns = ['school_code', 'lat', 'lon']
regions = regions.loc[:, ["Numéro d'école", 'code région']]
regions.columns = ['school_code', 'region_code']

df = positions.merge(regions, on='school_code')
df['region_code'] = df['region_code'].apply(lambda x: f'{x:1.0f}')

df.to_csv('clean_school_positions.csv', index=False)