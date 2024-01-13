class ModelData:
    '''This class defines the data structure of patient information that will be input into the prediction model'''
    age: int
    num_biopsies: int
    hyperplasia_status: int
    age_menstruation: int
    age_first_child: int
    num_relatives: int
    race: int
    birad_classification: int
    menopause_status: int

    def to_dict(self):
        '''Returns the information in a dictionary/json format that can be interpreted by the model'''
        
        return {
            "T1": self.age,
            "N_Biop": self.num_biopsies,
            "HypPlas": self.hyperplasia_status,
            "AgeMen": self.age_menstruation,
            "Age1st": self.age_first_child,
            "N_Rels": self.num_relatives,
            "Race": self.race,
            "BiRads": self.birad_classification,
            "menopause_status": self.menopause_status
        }