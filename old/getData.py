import pandas as pd

df = pd.read_csv('fr-en-effectifs-premier-degre.csv', sep=";", low_memory=False)
df.insert(1, 'My 2nd new column', '')
already_in_json = []
json_total = []

for ind in df.index:
    newjson = dict()
    print(df)
    newjson['Année scolaire'] = df['Année scolaire'][ind]
    newjson["Numéro d'école"] = df["Numéro d'école"[ind]

# new_json["Académie"] = df['Académie'][ind]
# new_json["Type d'établissement"] = df["Type d'établissement"][ind]
# new_json['Secteur Public/Privé'] = df['Secteur Public/Privé'][ind]
# new_json["Secteur d'enseignement"] = df["Secteur d'enseignement"][ind]
# new_json["Nombre d'élèves"] = df["Nombre d'élèves"][ind]
# new_json["libellé région"] = df["libellé région"][ind]
# new_json["code région"] = df["code région"][ind]
# new_json["Code département"] = df["Code département"][ind]
# new_json["Département"] = df["Département"][ind]
# already_in_json.append(code)