import json
import streamlit as st
from src.patient_data import PatientData
from src.Model.ModelController import ModelController
from src.Model.ModelData import ModelData

class AnalysisPageInterface:
    '''
    This class will handle the user interface for the analysis page and handle capturing the information input by users
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
            "atypical_hyperplasia_status": None,
            "birad_classification": None
        }


    def display(self):

        st.markdown(
        """
        # Breast Cancer Risk Evaluation

        ### Upload a mammmogram and input your information, our model will evaluate the risk of breast cancer :computer:
        """
        )

        with open('src/options_config.json', 'r') as config_file:
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
            else:
                birad_classification = self.model_controller.predict_birad_classification(self.patient_info["mammogram_image"])
                self.patient_info["birad_classification"] = birad_classification

            # Set the patient data to the inputs attained from the UI
            self.patient_data.set_data(**self.patient_info)
            self.handle_submit()

    def handle_submit(self):
        '''This function handles the logic when the submit button is pressed'''
        st.write(f":green[Information Submitted Successfully]")
   
        # Transform the questionnaire data into the format for the risk model
        input_data = self.model_controller.generate_input_data(self.patient_data)

        # Predict the risk of breast cancer 
        risk_output = self.model_controller.predict_risk(input_data)
        self.generate_evaluation(risk_output)

    def generate_evaluation(self, risk_output):
        '''This function generates an evaluation based on the risk_output.'''

        # Extracting the values from the risk_output dictionary
        risk_5_year = risk_output["5 Year risk figure"]
        risk_lifetime = risk_output["Lifetime risk figure"]
        qual_risk_5_year = risk_output["Qualitative 5 year risk"]
        qual_risk_lifetime = risk_output["Qualitative lifetime risk"]

        # Providing a general introduction to the evaluation
        st.write("## Breast Cancer Risk Assessment")
        st.write("Your breast cancer risk assessment is based on several factors and provides both a quantitative and a qualitative evaluation.")
        # Mapping of numeric BiRad classifications to their respective categories
        birad_mapping = {1: "A", 2: "B", 3: "C", 4: "D"}

        # Get the BiRad classification from patient data
        birad_classification = self.patient_data.birad_classification
        birad_category = birad_mapping.get(birad_classification, None)

        # Write the statement with the BiRad classification
        if birad_category is not None:
            st.write(f"According to our Convolutional Neural Network, your mammogram reveals that you have a BiRad classification of: {birad_category}.")
        else: 
            st.write(f"Please upload a mammogram so our model can determine your Birad category")

        # Displaying the quantitative risk with highlighted numbers
        st.markdown("### Quantitative Risk Assessment")
        st.markdown(f"- **5-Year Risk**: <span style='font-size: large;'><b>{risk_5_year:.2f}%</b></span> chance of developing breast cancer in the next 5 years.", unsafe_allow_html=True)
        st.markdown(f"- **Lifetime Risk**: <span style='font-size: large;'><b>{risk_lifetime:.2f}%</b></span> chance of developing breast cancer in your lifetime.", unsafe_allow_html=True)

        # Displaying the qualitative risk
        st.write("### Qualitative Risk Assessment")
        st.write(f"- **5-Year Risk Category**: Your risk is categorized as **{qual_risk_5_year}** for the next 5 years.")
        st.write(f"- **Lifetime Risk Category**: Your risk is categorized as **{qual_risk_lifetime}** over your lifetime.")

        # Providing additional guidance or recommendations based on the risk
        st.write("### Recommendations")
        if qual_risk_5_year == "High" or qual_risk_lifetime == "High":
            st.write("Given the high risk category, it's recommended to discuss with a healthcare provider for further assessment and possible screening options.")
        else:
            st.write("Continue with regular screenings and check-ups as recommended by your healthcare provider.")
        
        st.write("Please note that these assessments are based on statistical models and should not replace professional medical advice.")


