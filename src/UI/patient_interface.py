import streamlit as st
from ..patient_data import PatientData

class PatientInputInterface:
    def __init__(self):
        self.patient_data = PatientData()

    def display(self):
        st.title("Patient Health Data Input")

        # Patient details input
        age = st.slider("Age", min_value=35, max_value=90, step=1)
        ethnicity = st.selectbox("Ethnicity", ["Select", "Asian", "African", "Caucasian", "Hispanic", "Other"])
        smoker = st.radio("Smoker", ["Yes", "No"])
        country = st.text_input("Country")

        # Mammogram image upload
        mammogram_image = st.file_uploader("Upload Mammogram Image", type=["jpg", "jpeg", "png"])

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
