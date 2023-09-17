import numpy as np
import pandas as pd
import random

if __name__ == "__main__" :
    cities = pd.read_json('data/cities.json')
    cities.set_index('Name', inplace=True)
    cities.rename(columns={"choosenCoef":"choosenCoefCity"}, inplace=True)

    specialities = pd.read_json('data/specialities.json')
    specialities.set_index("Id", inplace=True)
    specialities.rename(columns={"choosenCoef":"choosenCoefSpec"}, inplace=True)

    combinaison = cities.merge(specialities, how="cross")


    print(specialities.head())
    print(cities.head())
    print(combinaison.head())
    print(combinaison.shape)