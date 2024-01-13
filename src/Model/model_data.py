class ModelData:
    '''This class defines the data structure of patient information that will be input into the prediction model'''
    T1: int
    N_Biop: int
    HypPlas: int
    AgeMen: int
    Age1st: int
    N_Rels: int
    Race: int
    BiRads: int
    menopause_status: int

    def to_dict(self):
        '''Returns the information in a dictionary/json format that can be interpreted by the model'''
        
        return {
            "T1": self.T1,
            "N_Biop": self.N_Biop,
            "HypPlas": self.HypPlas,
            "AgeMen": self.AgeMen,
            "Age1st": self.Age1st,
            "N_Rels": self.N_Rels,
            "Race": self.Race,
            "BiRads": self.BiRads,
            "menopause_status": self.menopause_status
        }