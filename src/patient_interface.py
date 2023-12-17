import streamlit as st

class PatientInputInterface:
    def __init__(self):
        self.age = None
        self.ethnicity = None
        self.smoker = None
        self.country = None
        self.mammogram_image = None

    def display(self):
        st.title("Patient Health Data Input")

        # Patient details input
        self.age = st.number_input("Age", min_value=0, max_value=130, step=1)
        self.ethnicity = st.selectbox("Ethnicity", ["Select", "Asian", "African", "Caucasian", "Hispanic", "Other"])
        self.smoker = st.radio("Smoker", ["Yes", "No"])
        self.country = st.text_input("Country")

        # Mammogram image upload
        self.mammogram_image = st.file_uploader("Upload Mammogram Image", type=["jpg", "jpeg", "png"])

        # Submit button
        if st.button("Submit"):
            self.handle_submit()

    def handle_submit(self):
        # Here you can add code to handle the data after submission
        st.write("Data Submitted:")
        st.write(f"Age: {self.age}")
        st.write(f"Ethnicity: {self.ethnicity}")
        st.write(f"Smoker: {self.smoker}")
        st.write(f"Country: {self.country}")
        if self.mammogram_image is not None:
            st.image(self.mammogram_image, caption="Uploaded Mammogram", use_column_width=True)
