from objects.Woman import Woman

class NCWoman (Woman):

    def __init__(self, age, BMI , status, phase, cortisol, sAA):
        super().__init__(Woman)
        self.phase = phase
        self.cortisol = cortisol
        self.sAA = sAA
        
