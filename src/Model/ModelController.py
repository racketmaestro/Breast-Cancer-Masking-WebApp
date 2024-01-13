import io
import numpy as np
import pandas as pd
import streamlit as st
from keras.models import load_model
from src.patient_data import PatientData
from src.Model.ModelData import ModelData
from PIL import Image
from src.Model.Gail_ModelV5 import RiskModel

class ModelController:

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
        model_data.T1 = patient_data.age
        model_data.AgeMen = patient_data.age_men
        model_data.Age1st = patient_data.age_at_first_child if patient_data.age_at_first_child is not None else 98
        model_data.BiRads = patient_data.birad_classification

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
        except Exception as e:
            st.error(f"An error occurred while trying to predict BiRads classification: {e}")

        # Set the classification to the category with highest probability. + 1 since zero-index
        birads_classification = np.argmax(prediction) + 1 

        return birads_classification

    # def predict_cancer(self, uploaded_file):
    #     # Read the file into a bytes-like object
    #     image_data = uploaded_file.read()

    #     # Open the image with PIL (ensures compatibility with different file types)
    #     image = Image.open(io.BytesIO(image_data))

    #     # Convert the image to grayscale if it's not already
    #     if image.mode != 'L':
    #         image = image.convert('L')

    #     # Resize the image
    #     image = image.resize((128, 128))

    #     # Convert the image to a numpy array
    #     image_array = np.array(image)
        
    #     # Expand dimensions to fit model's expected input
    #     image_array = np.expand_dims(image_array, axis=0)

    #     # Make prediction
    #     prediction = self.cancer_detection_model.predict(image_array)
        
    #     return prediction


