import pandas as pd

df = pd.read_csv('clased.tsv', sep="\t", low_memory=False)
df_pop = pd.read_csv('population2013.csv', sep=",", low_memory=False)
df['POPULATION'] = 0
errors = 0


for index, row in df.iterrows():
    population = 0
    communetoSearch = row.Commune
    code_extended = str(row['Code postal'])[:3]
    if int(row['Code postal'] >= 10000):
        code = str(row['Code postal'])[:2]
    else:
        code = '0' + str(row['Code postal'])[:1]

    # try:
    # i = df_pop.loc[df_pop['LIBGEO'] == str(communetoSearch)]
    i = df_pop.loc[df_pop['LIBGEO'] == str(communetoSearch)]
    for ct, r in i.iterrows():
        # if str(r[0][:2]) == code:
        if str(r[0]) == code or str(r[0]) == code_extended:
            population = r[2]
            break


    df.at[index,'POPULATION'] = population
    if population == 0:
        print(communetoSearch)
        errors += 1

print(errors)
df.to_csv("closedwithpop.csv", encoding='utf-8', index=False, sep=";")