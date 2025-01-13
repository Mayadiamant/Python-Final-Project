from objects.Woman import Woman

class HCWoman (Woman):

    def __init__(self, age, BMI , status, pill_type, cortisol, sAA):
        super().__init__(Woman)
        self.pill_type = pill_type
        self.cortisol = cortisol
        self.sAA = sAA
