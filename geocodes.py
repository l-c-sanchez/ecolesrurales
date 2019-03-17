"""
Converting address to GPS coordinates.
Using OpenStreetMapAPI

OpenStreetMap
https://wiki.openstreetmap.org/wiki/Nominatim
https://nominatim.openstreetmap.org/search?city=Paris&country=France&format=json

Opencage: 2500 request/day
https://opencagedata.com/pricing

Google maps: 1 request/day
Bing
"""

import pandas as pd
import requests
import time

from collections import namedtuple

Coordinates = namedtuple('Coordinates', ['latitude', 'longitude'])

class BandwithLimitException(Exception):
    pass

def find_coordinates(city, postal_code):
    base_url = 'https://nominatim.openstreetmap.org/search?'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

    params = {
        "postalcode": postal_code,
        "country": "France",
        "format": "json"
    }
    if city:
        params["city"] = city
    r = requests.get(base_url, params=params, headers={'User-Agent': user_agent})

    if r.status_code == 429:
        raise BandwithLimitException("Request has been blocked. We should wait for some time.")

    result = r.json()
    if result:
        result = result[0]
        return Coordinates(result["lat"], result["lon"]), result["display_name"], city is not None
    elif city:
        # Retry without city parameter
        return find_coordinates(None, postal_code)
    else:
        raise ValueError(f"No result found for postal code {postal_code}")



def normalize_postal_code(code):
    return "{:05d}".format(int(code))



print("Reading data.csv")
df = pd.read_csv("data.csv", sep=";")

# Keeping only closed schools
df = df[(df["2017-2018"] == "no")]

with open("geocodes.csv", "w") as f:
    with open("errors.csv", "w") as error_file:
        i = 1
        for index, row in df.iterrows():
            print(f"School {i} out of {df.shape[0]}")
            i += 1

            try:
                postal_code = normalize_postal_code(row["Code postal"])
                city = row["Commune"]
                school_id = row["Numéro d'école"]
                coordinates, display_name, city_used = find_coordinates(city, postal_code)
                f.write(";".join([school_id, coordinates.latitude, coordinates.latitude, display_name, str(city_used)]) + "\n")
            except BandwithLimitException:
                print("Stopping as we've been blocked by openstreetmap API")
                break
            except Exception as e:
                error_file.write(school_id + ";" + str(e) + "\n")
                print(e)

            time.sleep(2)



# row = df.iloc[385, :]
# postal_code = normalize_postal_code(row["Code postal"])
# city = row["Commune"]
# school_id = row["Numéro d'école"]
# coordinates, display_name, city_used = find_coordinates(city, postal_code)

