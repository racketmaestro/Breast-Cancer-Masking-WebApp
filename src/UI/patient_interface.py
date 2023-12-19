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

        # Basic input fields
        patient_info = {
            "age": st.slider("Age", **config['age_range']),
            "ageMen": st.slider("Age of first Menstrual Period", **config['age_men_range']),
            "ethnicity": st.selectbox("Ethnicity", config['ethnicities']),
            "relativesWithCancer": st.selectbox("Number of first degree relatives who had breast cancer", config['relatives_with_cancer']),
            "ageAtFirstChild": None,
            "numBenignDiagnoses": None,
            "atypicalHyperplasiaStatus": None,
            "mammogram_image": st.file_uploader("Upload Mammogram Image", type=config['file_types'])
        }

        # Conditional inputs
        if st.checkbox("Do you have a child?"):
            patient_info["ageAtFirstChild"] = st.slider("At what age did you have your first child?", 16, 50)

        biopsy_status = st.radio("Have you ever had a biopsy for breast cancer?", ('Yes', 'No', 'Unknown'))
        if biopsy_status == 'No':
            patient_info["numBenignDiagnoses"] = 0
        elif biopsy_status == 'Unknown':
            patient_info["numBenignDiagnoses"] = "Unknown"
        else:
            patient_info["numBenignDiagnoses"] = st.radio("How many breast biopsies with benign diagnoses:", ('1', '2 or more'))
            patient_info["atypicalHyperplasiaStatus"] = st.radio("Have you ever had a breast biopsy with atypical hyperplasia?", ('Yes', 'No', 'Unknown'))

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
