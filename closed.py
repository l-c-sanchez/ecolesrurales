import pandas as pd

df = pd.read_csv('clased.tsv', sep="\t", low_memory=False)
df_pop = pd.read_csv('populationvilles.csv', sep=",", low_memory=False)
df['POPULATION'] = 0
ct = 0

for index, row in df.iterrows():
    communetoSearch = row.Commune
    code = str(row['Code postal'])[:2]
    # print(code)

    # try:
    # i = df_pop.loc[df_pop['LIBGEO'] == str(communetoSearch)]
    i = df_pop.loc[df_pop['LIBGEO'] == str(communetoSearch)]
    print(i)
    population = i.POPULATION

    df.at[index,'POPULATION'] = population
    # except:
        # print("pb pour" + str(communetoSearch))
        # ct += 1
    print(i)
    # print(population)
    # df.at[index,'POPULATION'] = population

print(ct)
df.to_csv("closedwithpop.csv", encoding='utf-8', index=False, sep=";")