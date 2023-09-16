import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

url = "https://www.cngsante.fr/chiron/celine/finalnormcesp.html"

def getSpecialities(tableSoup : BeautifulSoup):
    specialitesId = []
    specialitesTotal = []

    spec = tableSoup.find_all("td", class_="tc")
    for s in spec :
        title = s.find("a")
        if title != None :
            titleId = title.get_text(strip=True)[0:3]
            specialitesId.append(titleId)

            titleTotal = title.find("span")
            if titleTotal != None :
                titleTotal = titleTotal.get_text(strip=True).replace("Ã©", "é")
                specialitesTotal.append(titleTotal)

    specialitesId, indId = np.unique(specialitesId, return_index=True)
    specialitesId = np.where(specialitesId=="BMB", "BM", specialitesId)

    specialitesTotal, indTotal = np.unique(specialitesTotal, return_index=True)
    return specialitesId[np.argsort(indId)], specialitesTotal[np.argsort(indTotal)]

def getCities(tableSoup : BeautifulSoup):
    cities = []
    cit = table.find_all("td", class_="rg")
    for c in cit :
        cities.append(c.get_text(strip=True).replace("Â", "").title())

    cities, ind = np.unique(cities, return_index=True)

    cities = np.where(cities=="Ap-Hp", "Paris", cities)
    cities = np.where(cities=="Hcl", "Lyon", cities)
    cities = np.where(cities=="Ap-Hm", "Marseille", cities)   

    return cities[np.argsort(ind)]

def getPlaces(tableSoup : BeautifulSoup, specLength : int, citiLength):
    places = np.zeros((citiLength, specLength))

    placeAvailable = tableSoup.find_all("td", class_="rk")
    i = 0
    for p in placeAvailable :
        places[i // specLength][i % specLength] = int(p.get_text(strip=True))
        i += 1

    return places

if __name__ == "__main__" :
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    
    table = soup.find_all("table")[0]

    specId, specDesc = getSpecialities(table)
    cities = getCities(table)

    places = getPlaces(table, len(specId), len(cities))

    df = pd.DataFrame(data=places, index=cities, columns=specId)
    df.to_pickle("data/placeAvailable.pkl")
