from abc import ABC, abstractmethod

class Woman (ABC):

    def __init__(self, age, BMI , status, cortisol):
        self.age = age
        self.BMI = BMI
        self.status = status
        self.cortisol = cortisol
    @abstractmethod
    def cortisol_response_to_stress(cortisol):
        pass


         