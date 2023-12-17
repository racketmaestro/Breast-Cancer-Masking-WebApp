import streamlit as st

class PatientInputInterface:
    def __init__(self):
        if 'patient_data' not in st.session_state:
            # Initialize the session state for patient data
            st.session_state['patient_data'] = {
                'age': None,
                'ethnicity': None,
                'smoker': None,
                'country': None,
                'mammogram_image': None
            }

    def display(self):
        st.title("Patient Health Data Input")

        # Patient details input
        st.session_state['patient_data']['age'] = st.slider("Age", min_value=0, max_value=100, step=1)
        st.session_state['patient_data']['ethnicity'] = st.selectbox("Ethnicity", ["Select", "Asian", "African", "Caucasian", "Hispanic", "Other"])
        st.session_state['patient_data']['smoker'] = st.radio("Smoker", ["Yes", "No"])
        st.session_state['patient_data']['country'] = st.text_input("Country")

        # Mammogram image upload
        st.session_state['patient_data']['mammogram_image'] = st.file_uploader("Upload Mammogram Image", type=["jpg", "jpeg", "png"])

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


def main():
    interface = PatientInputInterface()
    interface.display()

if __name__ == "__main__":
    main()

