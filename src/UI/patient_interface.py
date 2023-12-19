import streamlit as st
from src.patient_data import PatientData
import json

class PatientInputInterface:
    def __init__(self):
        self.patient_data = PatientData()

    def display(self):
        st.title("Patient Health Data Input")

        with open('options_config.json', 'r') as config_file:
            config = json.load(config_file)

        # Initialize optional values
        ageAtFirstChild = None
        numBenignDiagnoses = None
        atypicalHyperplasiaStatus = None
        
        # add the options selection UI 
        age = st.slider("Age", **config['age_range'])
        ageMen = st.slider("Age of first Menstrual Period", **config['age_men_range'])
        ethnicity = st.selectbox("Ethnicity", config['ethnicities'])
        relativesWithCancer = st.selectbox("Number of first degree relatives who had breast cacner", config['relatives_with_cancer'])
        # Checkbox to ask if the user has a child
        has_child = st.checkbox("Do you have a child?") 

        # If the user has a child, show the slider to input age
        if has_child:
            ageAtFirstChild = st.slider("At what age did you have your first child?", 16, 50)

        biopsy_status = st.radio("Have you ever had a biopsy for breast cancer?", ('Yes', 'No', 'Unknown'))

        # Conditional questions based on the response to the main question
        if biopsy_status == 'Yes':
            # Question for the number of benign diagnoses
            numBenignDiagnoses = st.radio("How many breast biopsies with benign diagnoses:", ('1', '2 or more'))

            # Question for atypical hyperplasia
            atypicalHyperplasiaStatus = st.radio("Have you ever had a breast biopsy with atypical hyperplasia?",
                                            ('Yes', 'No', 'Unknown'))

        mammogram_image = st.file_uploader("Upload Mammogram Image", type=config['file_types'])

        # Submit button logic
        if st.button("Submit"):
            # if mammogram_image is None:
            #     st.error("Please   upload a mammogram")
            #     return
            self.patient_data.set_data(age, ageMen, ethnicity, relativesWithCancer, ageAtFirstChild, numBenignDiagnoses, atypicalHyperplasiaStatus, mammogram_image)
            self.handle_submit()

    def handle_submit(self):
        # Display the data
        data_summary = self.patient_data.get_data_summary()
        st.write("Data Submitted:")
        for key, value in data_summary.items():
            st.write(f"{key}: {value}")

        print(self.patient_data.age) ## testing the class instance
