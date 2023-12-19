class PatientData:
    ''' This class is reponsible for storing the patient data which will be inputs into the models
    '''

    def __init__(self):
        self.age = None
        self.ethnicity = None
        self.mammogram_image = None

    def set_data(self, age, ethnicity, mammogram_image):
        self.age = age
        self.ethnicity = ethnicity
        self.mammogram_image = mammogram_image

    # Test function
    def get_data_summary(self):
        return {
            "Age": self.age,
            "Ethnicity": self.ethnicity,
            "Mammogram Image": "Uploaded" if self.mammogram_image is not None else "Not Uploaded"
        }
