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
        self.menopause_status = None

    def set_data(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key,value)

    