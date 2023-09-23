import numpy as np
import pandas as pd
from assignment import *
import concurrent.futures
import random
from functools import partial
import time

SpecImportance = 3
CityImportance = 2

nbStudent = 9165
nbRequest = 30

def calculateCoef(choosenCoefCity:float, choosenCoefSpec:float, abilityToIgnoreCity:float) -> float:
    """Calculate the attractivity of a service (city + speciality)

    Args:
        choosenCoefCity (float): Attractivity of a city
        choosenCoefSpec (float): Attractivity of a speciality
        abilityToIgnoreCity (float): The ability to ignore the city for each speciality

    Returns:
        float: Attractivity of a service
    """
    return SpecImportance*choosenCoefSpec + CityImportance*choosenCoefCity*(1 -  abilityToIgnoreCity)

def generateAttractivityColumns(dataframe : pd.DataFrame):
    """generate 3 more columns : attractivity_raw, attractivity_pourcentage, attractivity_cumsum

    Args:
        dataframe (pd.DataFrame): dataframe of all possible service (In/Out)
    """
    Attractivity = []
    for service in dataframe.iterrows():
        Attractivity.append(calculateCoef(service[1]["choosenCoefCity"], service[1]["choosenCoefSpec"], service[1]["abilityToIgnoreCity"]))

    dataframe["attractivity_raw"] = Attractivity
    dataframe["attractivity_pourcentage"] = dataframe["attractivity_raw"] / np.sum(dataframe["attractivity_raw"])
    dataframe["attractivity_cumsum"] = np.cumsum(dataframe["attractivity_pourcentage"])

def generateAnAssignmentRequest(dataframe : pd.DataFrame, index : int) -> assignmentRequest :
    """generate one assignment request using the attractivity coef

    Args:
        dataframe (pd.DataFrame): dataframe of all possible service
        index (int): index of the request for the student

    Returns:
        assignmentRequest: assignment request generated
    """
    choice = random.random()
    for current in range(len(dataframe)) :
        if (dataframe["attractivity_cumsum"][current] >= choice) :
            return assignmentRequest(index, dataframe["idSpec"][current],dataframe["city"][current])
        
def generateStudentsRequest(dataframe : pd.DataFrame, numberRequests : int) -> np.ndarray :
    """generate all of the assignment request for one student

    Args:
        dataframe (pd.DataFrame): dataframe of all possible service
        numberRequests (int): number of requests for each student

    Returns:
        np.ndarray: array of all requests
    """ 
    requests = []
    for index in range(numberRequests):
        requests.append(generateAnAssignmentRequest(dataframe, index+1))

    return np.array(requests)

def generateStudent(dataframe : pd.DataFrame, numberRequests : int, student : student):
    """Generate one student

    Args:
        dataframe (pd.DataFrame): dataframe of all possible service
        numberRequests (int): number of requests
        student (student): student that will be filled
    """ 
    student.requests = generateStudentsRequest(dataframe, numberRequests)

def generateAllStudentRequest(dataframe : pd.DataFrame, numberStudents : int, numberRequests : int) -> np.ndarray:
    """generate requests for all students

    Args:
        dataframe (pd.DataFrame): dataframe of all possible service
        numberStudents (int): number of students
        numberRequests (int): number of requests

    Returns:
        np.ndarray: array of all students
    """
    students = []
    for s in range(numberStudents):
        students.append(student(s+1, np.zeros(1)))


    generateStudentPartial = partial(generateStudent, dataframe, numberRequests)
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor :
        executor.map(generateStudentPartial, students)
    
    return np.array(students)


if __name__ == "__main__" :
    random.seed()
    cities = pd.read_json('data/cities.json')
    #cities.set_index('Name', inplace=True)
    cities.rename(columns={"choosenCoef":"choosenCoefCity", "Name":"city"}, inplace=True)

    specialities = pd.read_json('data/specialities.json')
    #specialities.set_index("Id", inplace=True)
    specialities.rename(columns={"choosenCoef":"choosenCoefSpec", "Name":"spec", "Id" : "idSpec"}, inplace=True)


    combinaison = cities.merge(specialities, how="cross")

    generateAttractivityColumns(combinaison)
    start = time.perf_counter()
    print(generateAllStudentRequest(combinaison, nbStudent, nbRequest))
    stop = time.perf_counter()

    print(f'Finished in {round(stop-start, 2)} second(s)')

