import pandas as pd
import json
from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import time

# Département
# Latitude
# Longitude
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
        print(appellation, Adresse, CodePostal, Commune, errors)
        return(appellation, Adresse, CodePostal, Commune, errors)
    except Exception as e:
        print(e)
        errors.append(num)
        print(url)
        return("", "", "", "", errors)

df = pd.read_csv('fr-en-effectifs-premier-degre.csv', sep=";", low_memory=False)
df_adresse = pd.read_csv('fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.csv', sep=";", low_memory=False)


missing_codes = set(df["Numéro d'école"]) - set(df_adresse["Code établissement"])
errors = []
rows = []

print(f"{len(missing_codes)} missing codes")
for i, code in enumerate(missing_codes):
    print(i, code)
    appellation, adresse, code_postal, commune, errors = find(code, errors)
    row = {
        "appelation": appellation,
        "adresse": adresse,
        "code_postal": code_postal,
        "commune": commune
    }
    rows.append(row)

results = pd.DataFrame(rows)

results.to_csv("missing_codes_results.csv", index=False)

# df = pd.read_csv('data_adresse.csv', sep=";", low_memory=False)
# ct = 0

# def build_url(num):
#     url = "https://www.journaldesfemmes.fr/maman/ecole/etablissement-" + num
#     return(url)

# def find(url):
#     try:
#         response = urllib2.urlopen(url).read()
#         soup = BeautifulSoup(response, 'lxml')
#         appellation = soup.find('div', {'class':"marB20"}).find("h1").text
#         ensemble = soup.findAll('div', {'class':"marB20"})[3].find('tbody').find('tr').findAll('td')[1]
        
#         Adresse = str(ensemble).split("<br/>")[0].replace("<td>", "")
#         CodePostal = re.sub('[^0-9]','', str(ensemble).split("<br/>")[1])

#         Commune = str(ensemble).split("<br/>")[1].replace("</td>", "")
#         Commune = ''.join(i for i in Commune if not i.isdigit())[1:]
#     except:
#         print(url)


# for i in df.index:
#     # print(df["Num"][i])
#     url = build_url(df["Num"][i])
#     find(url)
#     time.sleep(1)
# print(ct)