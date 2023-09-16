import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json

url = "https://www.cngsante.fr/chiron/celine/finalnormcesp.html"

def getSpecialities(tableSoup : BeautifulSoup) -> (np.ndarray, np.ndarray):
    """Extract the different specialities from the webpage

    Args:
        tableSoup (BeautifulSoup): Soup of the table in the webpage

    Returns:
        np.ndarray: Specialities Id
        np.ndarray: Specialities Complete Name
    """
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

def getCities(tableSoup : BeautifulSoup) -> np.ndarray:
    """Extract the different cities from the webpage

    Args:
        tableSoup (BeautifulSoup): Soup of the table in the webpage

    Returns:
        np.ndarray: Cities Names
    """
    cities = []
    cit = tableSoup.find_all("td", class_="rg")
    for c in cit :
        cities.append(c.get_text(strip=True).replace("Â", "").title())

    cities, ind = np.unique(cities, return_index=True)

    cities = np.where(cities=="Ap-Hp", "Paris", cities)
    cities = np.where(cities=="Hcl", "Lyon", cities)
    cities = np.where(cities=="Ap-Hm", "Marseille", cities)   

    return cities[np.argsort(ind)]

def getPlaces(tableSoup : BeautifulSoup, specLength : int, citiLength : int) -> np.ndarray:
    """Extract the number of availables places for all specialities in all cities

    Args:
        tableSoup (BeautifulSoup): Soup of the table in the webpage
        specLength (int): Number of specialities
        citiLength (int): Number of cities

    Returns:
        np.ndarray: Matrix of all the available places
    """
    places = np.zeros((citiLength, specLength))

    placeAvailable = tableSoup.find_all("td", class_="rk")
    i = 0
    for p in placeAvailable :
        places[i // specLength][i % specLength] = int(p.get_text(strip=True))
        i += 1

    return places

def saveSpecialitiesJson(specId : np.ndarray, specDesc : np.ndarray) -> None:
    """Save a json of all specialities with configurable variables

    Args:
        specId (np.ndarray): Specialities IDs
        specDesc (np.ndarray): Specialities Complete Names
    """
    specDict = []
    for i in range(len(specId)):
        sDict = {"Id":specId[i], "Name":specDesc[i], "choosenCoef" : 1, "abilityToIgnoreCity" : 0}
        specDict.append(sDict)

    with (open("data/specialities.json", "w") as f):
        f.write(json.dumps(specDict, ensure_ascii=False, indent=2))

def saveCitiesJson(cities : np.ndarray) -> None :
    """Save a json of all cities with configurable variables

    Args:
        cities (np.ndarray): Cities Names
    """
    citiesDict = []
    for i in range(len(cities)):
        cDict = {"Name":cities[i], "choosenCoef" : 1}
        citiesDict.append(cDict)

    with (open("data/cities.json", "w") as f):
        f.write(json.dumps(citiesDict, ensure_ascii=False, indent=2))


if __name__ == "__main__" :
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    table = soup.find_all("table")[0]

    specId, specDesc = getSpecialities(table)
    cities = getCities(table)

    places = getPlaces(table, len(specId), len(cities))

    df = pd.DataFrame(data=places, index=cities, columns=specId)
    df.to_pickle("data/placeAvailable.pkl")

    saveSpecialitiesJson(specId, specDesc)
    saveCitiesJson(cities)

