import pandas as pd
import json
from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import time
import geocoder

# Département
# Latitude
# Longitude

df = pd.read_csv('data_adresse.csv', sep=";", low_memory=False)
ct = 0

def build_url(num):
    url = "https://www.journaldesfemmes.fr/maman/ecole/etablissement-" + num
    return(url)

def find(url):
    try:
        response = urllib2.urlopen(url).read()
        soup = BeautifulSoup(response, 'lxml')
        appellation = soup.find('div', {'class':"marB20"}).find("h1").text
        ensemble = soup.findAll('div', {'class':"marB20"})[3].find('tbody').find('tr').findAll('td')[1]
        
        Adresse = str(ensemble).split("<br/>")[0].replace("<td>", "")
        CodePostal = re.sub('[^0-9]','', str(ensemble).split("<br/>")[1])

        Commune = str(ensemble).split("<br/>")[1].replace("</td>", "")
        Commune = ''.join(i for i in Commune if not i.isdigit())[1:]
    except:
        print(url)


for i in df.index:
    # print(df["Num"][i])
    url = build_url(df["Num"][i])
    find(url)
    time.sleep(1)
print(ct)