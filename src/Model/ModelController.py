import sys
sys.path.insert(0, 'C://Users//amosk//GitHub//Breast-Cancer-Masking-WebApp')
import io
from keras.models import load_model
from src.patient_data import PatientData
from src.Model.ModelData import ModelData
from PIL import Image
import numpy as np

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

        try:
            # Adjust the path according to your file structure
            model_path = 'src/Model/CancerDetectionModel.h5'
            self.cancer_detection_model = load_model(model_path)
        except Exception as e:
            # Handle exceptions (file not found, model loading errors, etc.)
            print(f"An error occurred while loading the cancer detection model: {e}")
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

        # model_data.Birad = [Insert code to get the breast density classification]
        model_data.Birad = 1

        return model_data

    def predict_risk(self, ModelData):
        model_data_json = ModelData.to_dict()

        pass

    def predict_cancer(self, uploaded_file):
        # Read the file into a bytes-like object
        image_data = uploaded_file.read()

        # Open the image with PIL (ensures compatibility with different file types)
        image = Image.open(io.BytesIO(image_data))

        # Convert the image to grayscale if it's not already
        if image.mode != 'L':
            image = image.convert('L')

        # Resize the image
        image = image.resize((128, 128))

        # Convert the image to a numpy array
        image_array = np.array(image)
        
        # Expand dimensions to fit model's expected input
        image_array = np.expand_dims(image_array, axis=0)

        # Make prediction
        prediction = self.cancer_detection_model.predict(image_array)
        
        return prediction


# def main():
#     model_controller = ModelController()
#     patient_data = PatientData()
#     patient_data.set_data(age=30, age_men=13, ethnicity="Chinese", relatives_with_cancer="One", 
#                      age_at_first_child=25, num_benign_diagnoses='One', 
#                      atypical_hyperplasia_status='Unknown', mammogram_image=None)
#     patient_model_data = model_controller.generate_input_data(patient_data)
#     patient_data_json = patient_model_data.to_dict()
#     print(patient_data_json)
    
#     im = tf.io.read_file('A_0005_1.LEFT_MLO.jpg')
#     prediction = model_controller.predict_cancer(im)
#     print(prediction)


# if __name__ == "__main__":
#     main()
