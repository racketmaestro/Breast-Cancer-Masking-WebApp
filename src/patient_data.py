class PatientData:
    def __init__(self):
        self.age = None
        self.ethnicity = None
        self.smoker = None
        self.country = None
        self.mammogram_image = None

    def set_data(self, age, ethnicity, smoker, country, mammogram_image):
        self.age = age
        self.ethnicity = ethnicity
        self.smoker = smoker
        self.country = country
        self.mammogram_image = mammogram_image

    # Test function
    def get_data_summary(self):
        return {
            "Age": self.age,
            "Ethnicity": self.ethnicity,
            "Smoker": self.smoker,
            "Country": self.country,
            "Mammogram Image": "Uploaded" if self.mammogram_image is not None else "Not Uploaded"
        }
