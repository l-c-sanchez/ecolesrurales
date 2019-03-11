import pandas as pd
# import bs4 as BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import json

# def find_adresse(num):
#     url = "https://www.google.com/search?client=ubuntu&channel=fs&q=" + num + "&ie=utf-8&oe=utf-8"
#     print(url)
#     try:
#         headers = {"User-Agent":"Mozilla/5.0"}
#         response = requests.get(url, headers=headers, timeout=5)
#         soup = bs4.BeautifulSoup(response.text, 'lxml')
#     except:
#         print("in except")

df = pd.read_csv('fr-en-effectifs-premier-degre.csv', sep=";", low_memory=False)
df_adresse = pd.read_csv('fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.csv', sep=";", low_memory=False)
already_csv = []
already_adresse = []
csv_total = []
no_adresse = []

for i in df_adresse.index:
    already_adresse.append(df_adresse["Code établissement"][i])

for ind in df.index:
    new = dict()
    if df["Numéro d'école"][ind] in already_csv:
        index = already_csv.index(df["Numéro d'école"][ind])
        csv_total[index][df["Année scolaire"][ind]] = "yes"
        csv_total[index]["Nombre d'élèves " + df["Année scolaire"][ind]] = df["Nombre d'élèves"][ind]
        if csv_total[index]["Académie"] == "":
            csv_total[index]["Académie"] = df["Académie"][ind]
            csv_total[index]["Code département"] = df["Code département"][ind]
            csv_total[index]["Département"] = df["Département"][ind]

    else:
        new["Numéro d'école"] = df["Numéro d'école"][ind]
        if df["Numéro d'école"][ind] in already_adresse:
            i = already_adresse.index(df["Numéro d'école"][ind])
            new["Adresse"] = df_adresse["Adresse"][i]
            new["Lieu dit"] = df_adresse["Lieu dit"][i]
            new["Boite postale"] = df_adresse["Boite postale"][i]
            new["Code postal"] = df_adresse["Code postal"][i]
            new["Commune"] = df_adresse["Commune"][i]
            new["Coordonnee X"] = df_adresse["Coordonnee X"][i]
            new["Coordonnee Y"] = df_adresse["Coordonnee Y"][i]
            new["Latitude"] = df_adresse["Latitude"][i]
            new["Longitude"] = df_adresse["Longitude"][i]
            new["Appellation officielle"] = df_adresse["Appellation officielle"][i]
            new["Patronyme uai"] = df_adresse["Patronyme uai"][i]
        else:
            no_adresse.append(df["Numéro d'école"][ind])
            # driver = webdriver.Firefox()
            # driver.get("http://www.python.org")
        new["2015-2016"] = "no"
        new["2016-2017"] = "no"
        new["2017-2018"] = "no"
        new[df["Année scolaire"][ind]] = "yes"
        new["Académie"] = df["Académie"][ind]
        new["Secteur d'enseignement"] = df["Secteur d'enseignement"][ind]
        new["Nombre d'élèves " + df["Année scolaire"][ind]] = df["Nombre d'élèves"][ind]
        new["libellé région"] = df["libellé région"][ind]
        new["code région"] = df["code région"][ind]
        new["Code département"] = df["Code département"][ind]
        new["Département"] = df["Département"][ind]
        already_csv.append(df["Numéro d'école"][ind])
        csv_total.append(new)

df = pd.DataFrame(csv_total)
df_2 = pd.DataFrame(no_adresse)
df.to_csv("data.csv", encoding='utf-8', index=False, sep=";")
try:
    df_2.to_csv("data_adresse.csv", encoding='utf-8', index=False)
except:
    print("no adresse")
