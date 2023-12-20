import json
import streamlit as st
from src.patient_data import PatientData

class PatientInputInterface:
    '''
    '''
    def __init__(self):

        # Instantiate a patient session
        self.patient_data = PatientData()

    def display(self):
        st.title("Dilcock Health")

        with open('options_config.json', 'r') as config_file:
            config = json.load(config_file)

        # Basic input fields
        patient_info = {
            "mammogram_image": st.file_uploader("Upload Mammogram Image", type=config['file_types']),
            "age": st.slider("Age", **config['age_range']),
            "ageMen": st.slider("Age of first Menstrual Period", **config['age_men_range']),
            "ethnicity": st.selectbox("Ethnicity", config['ethnicities']),
            "relativesWithCancer": st.selectbox("Number of first degree relatives who had breast cancer", config['relatives_with_cancer']),
            "ageAtFirstChild": None,
            "numBenignDiagnoses": None,
            "atypicalHyperplasiaStatus": None
        }

        # Conditional inputs
        if st.checkbox("Tick if you have a child/children"):
            patient_info["ageAtFirstChild"] = st.slider("At what age did you have your first child?", **config['age_first_child'])

        biopsy_status = st.radio("Have you ever had a biopsy for breast cancer?", config['biopsy_status'])
        if biopsy_status == 'No':
            patient_info["numBenignDiagnoses"] = '0'
        elif biopsy_status == 'Unknown':
            patient_info["numBenignDiagnoses"] = "Unknown"
        else:
            patient_info["numBenignDiagnoses"] = st.radio("How many breast biopsies with benign diagnoses:", config['num_benign_diagnoses'])
            patient_info["atypicalHyperplasiaStatus"] = st.radio("Have you ever had a breast biopsy with atypical hyperplasia?", config['atypical_hyperplasia_status'])

        # Submit button logic
        if st.button("Submit"):
            if patient_info["mammogram_image"] is None:
                st.error("Please upload a mammogram")   
                # return 
            self.patient_data.set_data(**patient_info)
            self.handle_submit()

    def handle_submit(self):
        # Display the data
        data_summary = self.patient_data.get_data_summary()
        st.write("Data Submitted:")
        for key, value in data_summary.items():
            st.write(f"{key}: {value}")

        print(self.patient_data.age) ## testing the class instance
