class ModelData:
    '''This class defines the data structure of patient information that will go into the prediction model'''
    T1: int
    N_Biop: int
    HypPlas: int
    AgeMen: int
    Age1st: int
    N_Rels: int
    Race: int
    Birad: int

    def to_dict(self):
        return {
            "T1": self.T1,
            "N_Biop": self.N_Biop,
            "HypPlas": self.HypPlas,
            "AgeMen": self.AgeMen,
            "Age1st": self.Age1st,
            "N_Rels": self.N_Rels,
            "Race": self.Race,
            "Birad": self.Birad
        }