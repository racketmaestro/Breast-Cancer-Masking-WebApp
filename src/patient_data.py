class PatientData:
    ''' This class is reponsible for storing the patient data which will be inputs into the models
    '''

    def __init__(self):
        self.age = None
        self.age_men = None
        self.ethnicity = None
        self.relatives_with_cancer = None
        self.age_at_first_child = None
        self.num_benign_diagnoses = None
        self.atypical_hyperplasia_status = None
        self.mammogram_image = None
        self.birad_classification = None

    def set_data(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key,value)

    # Test function
    def get_data_summary(self):
        return {
            "Age": self.age,
            "Agemen" : self.age_men,
            "Ethnicity": self.ethnicity,
            "Relatives with cancer": self.relatives_with_cancer,
            "Age at first child": self.age_at_first_child,
            "Number of benign diagnoses" : self.num_benign_diagnoses,
            "Atypical Hyperplasia Status": self.atypical_hyperplasia_status,
            "Mammogram Image": "Uploaded" if self.mammogram_image is not None else "Not Uploaded"
        }
    