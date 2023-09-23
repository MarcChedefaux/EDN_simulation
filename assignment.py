import numpy as np

class assignmentRequest :
    def __init__(self, index:int, idSpec : str, city : str ) :
        """Init for class assignmentRequest

        Args:
            index (int): index of the request
            idSpec (str): id of the speciality
            city (str): id of the city
        """
        self.index = index
        self.spec = idSpec
        self.city = city

    def __str__(self):
        """to string for assignment request

        Returns:
            string: string description of assignment request
        """
        return f"Assignment request n°{self.index} : {self.spec} at {self.city}"
    
    def __repr__(self):
        """to representation for assignment request

        Returns:
            string: string representation of assignment request
        """
        return f"assignmentRequest({self.index}, {self.spec},{self.city})"
    
class student : 
    def __init__(self, classement:int, requests:np.ndarray):
        """Init for class student

        Args:
            classement (int): classement of the student
            requests (np.ndarray): requests of the student
        """
        self.classement = classement
        self.requests = requests

    def __str__(self):
        """to string for student

        Returns:
            string: string description of student
        """
        return f"Student n°{self.classement} : {self.requests}"
    
    def __repr__(self):
        """to representation for student

        Returns:
            string: string representation of student
        """
        return f"Student({self.classement},{self.requests})"
