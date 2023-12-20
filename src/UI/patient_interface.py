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
        left_col, right_col = st.columns(2)

        left_col.markdown("# Dilcock Health")
        left_col.markdown("### A tool for analyzing risk of breast cancer")
        left_col.markdown("**Created by Silcock and Sons**")
        left_col.markdown("**Amos Koh, Cameron Briginshaw, Aveek Goswami, Wei Han Low, David Silcock**")


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

        # Basic input fields
        patient_info = {
            "mammogram_image": st.file_uploader("Upload Mammogram Image", type=config['file_types']),
            "age": st.slider("Age", **config['age_range']),
            "age_men": st.slider("Age of first Menstrual Period", **config['age_men_range']),
            "ethnicity": st.selectbox("Ethnicity", config['ethnicities']),
            "relatives_with_cancer": st.selectbox("Number of first degree relatives who had breast cancer", config['relatives_with_cancer']),
            "age_at_first_child": None,
            "num_benign_diagnoses": None,
            "atypical_hyperplasia_status": None
        }

        # Conditional inputs
        if st.checkbox("Tick if you have a child/children"):
            patient_info["age_at_first_child"] = st.slider("At what age did you have your first child?", **config['age_first_child'])

        biopsy_status = st.radio("Have you ever had a biopsy for breast cancer?", config['biopsy_status'])
        if biopsy_status == 'No':
            patient_info["num_benign_diagnoses"] = '0'
        elif biopsy_status == 'Unknown':
            patient_info["num_benign_diagnoses"] = "Unknown"
        else:
            patient_info["num_benign_diagnoses"] = st.radio("How many breast biopsies with benign diagnoses:", config['num_benign_diagnoses'])
            patient_info["atypical_hyperplasia_status"] = st.radio("Have you ever had a breast biopsy with atypical hyperplasia?", config['atypical_hyperplasia_status'])

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
