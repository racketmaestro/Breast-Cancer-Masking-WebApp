import sys
sys.path.insert(0, 'C://Users//amosk//GitHub//Breast-Cancer-Masking-WebApp')

from src.patient_data import PatientData
from src.Model.ModelData import ModelData

class ModelController:

    # Define integer representations for race
    RACE_MAPPING = {
        "White":1,
        "African-American":2,
        "Hispanic US Born":3,
        "Native American":4,
        "Hispanic/Latina":5,
        "Chinese":6,
        "Japanese":7,
        "Filipino":8,
        "Hawaiian":9,
        "Other Pacific Islander":10,
        "Other Asian":11
    }

    # Define integer representations for relatives
    RELATIVES_MAPPING = {
        "None": 0,
        "One": 1,
        "More than one": 2
    }


    def __init__(self) -> None:
        pass

    def generate_input_data(self, patient_data: PatientData) -> ModelData:
        '''This function will transform the questionnaire answers into formats
        compatible with the model, and return the ModelData data class'''

        model_data = ModelData()
        model_data.T1 = patient_data.age
        model_data.AgeMen = patient_data.age_men
        model_data.Age1st = patient_data.age_at_first_child if not None else 99
        
        # Map number of relatives answer to an integer
        model_data.N_Rels = ModelController.RELATIVES_MAPPING.get(patient_data.relatives_with_cancer, 99)

        # Default values for both variables
        model_data.N_Biop = 99
        model_data.HypPlas = 99

        # Update N_Biop based on num_benign_diagnoses
        if patient_data.num_benign_diagnoses == "0":
            model_data.N_Biop = 0
        elif patient_data.num_benign_diagnoses == "One":
            model_data.N_Biop = 1
        elif patient_data.num_benign_diagnoses == "Two or more":
            model_data.N_Biop = 2

        # Update HypPlas based on atypical_hyperplasia_status if num_benign_diagnoses is known
        if patient_data.num_benign_diagnoses != "Unknown":
            if patient_data.atypical_hyperplasia_status == "Yes":
                model_data.HypPlas = 1
            elif patient_data.atypical_hyperplasia_status == "No":
                model_data.HypPlas = 0


        # Map race answer to an integer
        model_data.Race = ModelController.RACE_MAPPING.get(patient_data.ethnicity)

        return model_data

    def predict_risk(self, ModelData):
        model_data_json = ModelData.to_dict()

        pass

    def load_model(self):
        pass

def main():
    model_controller = ModelController()
    patient_data = PatientData()
    patient_data.set_data(age=30, age_men=13, ethnicity="Chinese", relatives_with_cancer="One", 
                     age_at_first_child=25, num_benign_diagnoses='One', 
                     atypical_hyperplasia_status='Unknown', mammogram_image=None)
    patient_model_data = model_controller.generate_input_data(patient_data)
    patient_data_json = patient_model_data.to_dict()
    print(patient_data_json)
    
    print("OK")


if __name__ == "__main__":
    main()
