import sys
sys.path.insert(0, 'C://Users//amosk//GitHub//Breast-Cancer-Masking-WebApp')
from src.patient_data import PatientData
from src.Model.ModelData import ModelData
from dataclasses import dataclass

class ModelController:
    def __init__(self) -> None:
        pass

    def generate_input_data(self, PatientData) -> ModelData:
        '''This function will transform the questionnaire answers into formats
        compatible with the model, and return the ModelData data class'''

        model_data = ModelData()
        model_data.T1 = PatientData.age
        model_data.AgeMen = PatientData.age_men
        model_data.Age1st = PatientData.age_at_first_child if not None else 99
        
        # Define mappings for relatives_with_cancer
        relatives_mapping = {
            "None": 0,
            "One": 1,
            "More than one": 2
        }
   
        model_data.N_Rels = relatives_mapping.get(PatientData.relatives_with_cancer, 99)

        if PatientData.num_benign_diagnoses == "Unknown":
            model_data.N_Biop = 99
            model_data.HypPlas = 99
        elif PatientData.num_benign_diagnoses == 0:
            model_data.N_Biop = 0
            model_data.HypPlas = 99
        elif PatientData.num_benign_diagnoses == "1":
            model_data.N_Biop = 1
            if PatientData.atypical_hyperplasia_status == "Yes":
                model_data.HypPlas = 1
            elif PatientData.atypical_hyperplasia_status == "No":
                model_data.HypPlas = 0
            else:
                model_data.HypPlas = 99
        elif PatientData.num_benign_diagnoses == "2 or more":
            model_data.N_Biop = 2 
            if PatientData.atypical_hyperplasia_status == "Yes":
                model_data.HypPlas = 1
            elif PatientData.atypical_hyperplasia_status == "No":
                model_data.HypPlas = 0
            else:
                model_data.HypPlas = 99

        # Map Race to a integer weightage
        race_mapping = {
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

        model_data.Race = race_mapping.get(PatientData.ethnicity)

        return model_data

    def predict_risk(self, ModelData):
        model_data_json = ModelData.to_dict()

        pass

    def load_model(self):
        pass

def main():
    model_controller = ModelController()
    print("OK")


if __name__ == "__main__":
    main()
