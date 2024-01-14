import io
import numpy as np
import pandas as pd
import streamlit as st
from keras.models import load_model
from src.patient_data import PatientData
from src.Model.model_data import ModelData
from PIL import Image
from src.Model.risk_model import RiskModel

class ModelController:
    '''This class is the system which interacts with the risk prediction model and BI-RADS classification model.
    It also facilitates the flow and transformation of patient data and model data, which necessary for the models' functionalities.'''

    # Define integer representations for race
    RACE_MAPPING = {
        "White": 1,
        "African-American": 2,
        "Hispanic US Born": 3,
        "Native American": 4,
        "Hispanic/Latina": 5,
        "Chinese": 6,
        "Japanese": 7,
        "Filipino": 8,
        "Hawaiian": 9,
        "Other Pacific Islander": 10,
        "Other Asian": 11
    }

    # Define integer representations for relatives
    RELATIVES_MAPPING = {
        "None": 0,
        "One": 1,
        "More than one": 2
    }

    def __init__(self) -> None:

        try:
            # Load the birad classification model
            birad_model_path = 'src/Model/BiradClassificationModel.h5'
            self.birad_classification_model = load_model(birad_model_path)
        except Exception as e:
            # Handle exceptions
            print(f"An error occurred while loading the CNN model: {e}")
        pass

    def generate_input_data(self, patient_data: PatientData) -> ModelData:
        '''This function will transform the questionnaire answers into formats
        compatible with the model, and return the ModelData data class'''

        # Create new instance of ModelData class
        model_data = ModelData()

        # Populate the fields
        model_data.age = patient_data.age
        model_data.age_menstruation = patient_data.age_men
        model_data.age_first_child = patient_data.age_at_first_child if patient_data.age_at_first_child is not None else 98
        model_data.birad_classification = patient_data.birad_classification if patient_data.birad_classification is not None else 1

        # Map number of relatives answer to an integer
        model_data.num_relatives = ModelController.RELATIVES_MAPPING.get(patient_data.relatives_with_cancer, 99)

        # Default values for both variables
        model_data.num_biopsies = 99
        model_data.hyperplasia_status = 99

        # Update N_Biop based on num_benign_diagnoses
        if patient_data.num_benign_diagnoses == "0":
            model_data.num_biopsies = 0
        elif patient_data.num_benign_diagnoses == "One":
            model_data.num_biopsies = 1
        elif patient_data.num_benign_diagnoses == "Two or more":
            model_data.num_biopsies = 2

        # Update menopause_status
        model_data.menopause_status = 1 if patient_data.menopause_status == "Yes" else 0

        # Update HypPlas based on atypical_hyperplasia_status if num_benign_diagnoses is known
        if patient_data.num_benign_diagnoses != "Unknown":
            if patient_data.atypical_hyperplasia_status == "Yes":
                model_data.hyperplasia_status = 1
            elif patient_data.atypical_hyperplasia_status == "No":
                model_data.hyperplasia_status = 0

        # Map race answer to an integer
        model_data.race = ModelController.RACE_MAPPING.get(patient_data.ethnicity)

        return model_data

    def predict_risk(self, model_data: ModelData):
        '''This function will run the risk analysis using the Gail Model and the processed health data input by users'''
        
        model_data_json = model_data.to_dict()
        data = pd.DataFrame([model_data_json])

        try:
            risk_model = RiskModel(data)
            risk_output = risk_model.run_model()
        except Exception as e:
            st.error(f"An error occured while running risk evaluation, please report it to Silcock and Sons: {e}")
        
        return risk_output
    
    def predict_birad_classification(self, uploaded_file):
        '''This function will use the mammogram uploaded to predict the BiRads classification of the user'''

        # Initialise the default birad classification output
        birads_classification = None
        
        # Read the file into a bytes-like object
        image_data = uploaded_file.read()

        # Open the image with PIL (ensures compatibility with different file types)
        image = Image.open(io.BytesIO(image_data))

        # Convert the image to grayscale
        if image.mode != 'L':
            image = image.convert('L')

        # Transform the image to fit the model input requirements
        image = image.resize((128, 128))
        image_array = np.array(image)
        image_array = np.expand_dims(image_array, axis=0)

        # Predict probability of each BiRads classification
        try:
            prediction = self.birad_classification_model(image_array)
            
            # Set the classification to the category with highest probability. + 1 since zero-index
            birads_classification = np.argmax(prediction) + 1 

            # Check that the probability output is above a certain threshold
            probability_of_chosen_class = prediction[0, birads_classification - 1]
            print(prediction)
            if probability_of_chosen_class <= 0.8:
                st.error('''
                        Our model could not decisively predict your breast density based on the mammogram, 
                        perhaps check that you have uploaded the correct image or find another mammogram''')
                return 
            
        except Exception as e:
            st.error(f"An error occurred while trying to predict BiRads classification: {e}")

        return birads_classification

