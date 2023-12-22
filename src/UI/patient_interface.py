import json
import streamlit as st
from src.patient_data import PatientData
from src.Model.ModelController import ModelController

class PatientInputInterface:
    '''
    '''

    def __init__(self, model_controller: ModelController()):

        # Instantiate a patient data storage class
        self.patient_data = PatientData()  
        self.model_controller = model_controller

        # Initialize the patient_info dictionary. This is specific to the state session
        self.patient_info = {
            "mammogram_image": None,
            "age": None,
            "age_men": None,
            "ethnicity": None,
            "relatives_with_cancer": None,
            "age_at_first_child": None,
            "num_benign_diagnoses": None,
            "atypical_hyperplasia_status": None
        }

        # Initialize the patient_info dictionary. This is specific to the state session
        self.patient_info = {
            "mammogram_image": None,
            "age": None,
            "age_men": None,
            "ethnicity": None,
            "relatives_with_cancer": None,
            "age_at_first_child": None,
            "num_benign_diagnoses": None,
            "atypical_hyperplasia_status": None
        }

    def display(self):
        left_col, right_col = st.columns(2)

        left_col.markdown("# Dilcock Health")
        left_col.markdown("### A tool for analyzing risk of breast cancer")
        left_col.markdown("**Created by Silcock and Sons**")
        left_col.markdown("**Amos Koh, Cameron Briginshaw, Aveek Goswami, Wei Han Low, David Silcock**")

        # URL of the image
        image_url ='https://cdn.pixabay.com/photo/2020/05/25/03/37/doctor-5216835_1280.png'

        # Display the image in the right column
        right_col.image(image_url, caption='Mr Dilcock will see you now')

        st.markdown("---")

        st.markdown(
        """
        ### Summary
        *Dilcocks rule*
        """
        )

        st.markdown("---")

        with open('options_config.json', 'r') as config_file:
            config = json.load(config_file)

        # Update patient_info dictionary based on user input
        self.patient_info["mammogram_image"] = st.file_uploader("Upload Mammogram Image", type=config['file_types'])
        # Display the uploaded image
        if self.patient_info["mammogram_image"] is not None:
            # Display the uploaded file directly
            st.image(self.patient_info["mammogram_image"], caption='Uploaded Image', width=300)


        self.patient_info["age"] = st.slider("Age", **config['age_range'])
        self.patient_info["age_men"] = st.slider("Age of first Menstrual Period", **config['age_men_range'])
        self.patient_info["ethnicity"] = st.selectbox("Ethnicity", config['ethnicities'])
        self.patient_info["relatives_with_cancer"] = st.selectbox("Number of first degree relatives who had breast cancer", config['relatives_with_cancer'])

        # Conditional inputs
        if st.checkbox("Tick if you have a child/children"):
            self.patient_info["age_at_first_child"] = st.slider("At what age did you have your first child?", **config['age_first_child'])

        biopsy_status = st.radio("Have you ever had a biopsy for breast cancer?", config['biopsy_status'])
        if biopsy_status == 'No':
            self.patient_info["num_benign_diagnoses"] = '0'
        elif biopsy_status == 'Unknown':
            self.patient_info["num_benign_diagnoses"] = "Unknown"
        else:
            self.patient_info["num_benign_diagnoses"] = st.radio("How many breast biopsies with benign diagnoses:", config['num_benign_diagnoses'])
            self.patient_info["atypical_hyperplasia_status"] = st.radio("Have you ever had a breast biopsy with atypical hyperplasia?", config['atypical_hyperplasia_status'])

        # Submit button logic
        if st.button("Submit"):
            if self.patient_info["mammogram_image"] is None:
                st.error("Please upload a mammogram")   
                # return 
            self.patient_data.set_data(**self.patient_info)
            self.handle_submit()

    def handle_submit(self):
        '''This function handles the logic when the submit button is pressed'''
        st.write(f":green[Thank you for submitting your information]")

        if self.patient_info["mammogram_image"]:
            prediction = self.model_controller.predict_cancer(self.patient_info["mammogram_image"])
            # st.write(f"Chance of No cancer: :blue[{prediction[0][0]}], Chance of cancer: :blue[{prediction[0][1]}]")

            # Check for detection cancer
            if prediction[0][1] >= 0.8:
                st.write(f":red[YOU HAVE BREAST CANCER]")
            elif prediction[0][0]>= 0.8:
                st.write(f":green[No tumour growth detected]")
            if abs(prediction[0][1] - prediction[0][0]) < 0.7:
                st.markdown("<span style='background-color: #DFF2BF'>The model is inconclusive</span>, please upload another mammogram or check that you uploaded the correct file.", unsafe_allow_html=True)

        print(self.patient_data.age) ## testing the class instance
