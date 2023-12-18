import streamlit as st
from ..patient_data import PatientData
import json

class PatientInputInterface:
    def __init__(self):
        self.patient_data = PatientData()

    def display(self):
        st.title("Patient Health Data Input")

        with open('options_config.json', 'r') as config_file:
            config = json.load(config_file)

        age = st.slider("Age", **config['age_range'])
        ethnicity = st.selectbox("Ethnicity", config['ethnicities'])
        mammogram_image = st.file_uploader("Upload Mammogram Image", type=config['file_types'])
        smoker = st.radio("Smoker", config['smoker'])
        country = st.selectbox("Country", config['country'])

        # Submit button
        if st.button("Submit"):
            self.patient_data.set_data(age, ethnicity, smoker, country, mammogram_image)
            self.handle_submit()

    def handle_submit(self):
        # Display the data
        data_summary = self.patient_data.get_data_summary()
        st.write("Data Submitted:")
        for key, value in data_summary.items():
            st.write(f"{key}: {value}")

        print(self.patient_data.age) ## testing the class instance
