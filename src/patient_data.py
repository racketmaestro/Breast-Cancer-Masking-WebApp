class PatientData:
    ''' This class is reponsible for storing the patient data which will be inputs into the models
    '''

    def __init__(self):
        self.age = None
        self.ageMen = None
        self.ethnicity = None
        self.relativesWithCancer = None
        self.ageAtFirstChild = None
        self.numBenignDiagnoses = None
        self.atypicalHyperplasiaStatus = None
        self.mammogram_image = None

    def set_data(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key,value)

    # Test function
    def get_data_summary(self):
        return {
            "Age": self.age,
            "Agemen" : self.ageMen,
            "Ethnicity": self.ethnicity,
            "Relatives with cancer": self.relativesWithCancer,
            "Age at first child": self.ageAtFirstChild,
            "Number of benign diagnoses" : self.numBenignDiagnoses,
            "Atypical Hyperplasia Status": self.atypicalHyperplasiaStatus,
            "Mammogram Image": "Uploaded" if self.mammogram_image is not None else "Not Uploaded"
        }
    