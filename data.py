import pandas as pd
import json
import time

from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import time


def find(num, errors):
    url = "https://www.journaldesfemmes.fr/maman/ecole/etablissement-" + num
    try:
        response = urllib2.urlopen(url).read()
        soup = BeautifulSoup(response, 'lxml')
        appellation = soup.find('div', {'class':"marB20"}).find("h1").text
        ensemble = soup.findAll('div', {'class':"marB20"})[3].find('tbody').find('tr').findAll('td')[1]
        
        Adresse = str(ensemble).split("<br/>")[0].replace("<td>", "")
        CodePostal = re.sub('[^0-9]','', str(ensemble).split("<br/>")[1])

        Commune = str(ensemble).split("<br/>")[1].replace("</td>", "")
        Commune = ''.join(i for i in Commune if not i.isdigit())[1:]
        print(num)
        return(appellation, Adresse, CodePostal, Commune, errors)
    except Exception as e:
        print(e)
        errors.append(num)
        print(url)
        return("", "", "", "", errors)
        




df = pd.read_csv('fr-en-effectifs-premier-degre.csv', sep=";", low_memory=False)
df_adresse = pd.read_csv('fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.csv', sep=";", low_memory=False)
already_csv = []
already_adresse = []
csv_total = []
no_adresse = []
errors = []

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
            new["Etat établissement"] = df_adresse["Etat établissement"][i]
            new["Code postal"] = df_adresse["Code postal"][i]
            new["Commune"] = df_adresse["Commune"][i]
            new["Latitude"] = df_adresse["Latitude"][i]
            new["Longitude"] = df_adresse["Longitude"][i]
            new["Appellation officielle"] = df_adresse["Appellation officielle"][i]
            new["Patronyme uai"] = df_adresse["Patronyme uai"][i]
        else:
            time.sleep(0.2)
            no_adresse.append(df["Numéro d'école"][ind])
            new["Appellation officielle"], new["Adresse"], new["Code postal"], new["Commune"], errors = find(df["Numéro d'école"][ind], errors)

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
df_2.to_csv("data_adresse.csv", encoding='utf-8', index=False)

df_errors = pd.DataFrame(errors)
df_errors.to_csv("data_errorsbs4.csv", encoding='utf-8', index=False)
