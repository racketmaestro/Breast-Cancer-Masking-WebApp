import json
import streamlit as st
from src.patient_data import PatientData
from src.Model.model_controller import ModelController

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
            "birad_classification": None,
            "menopause_status" : None
        }


    def display(self):

        st.markdown(
        """
        # Breast Cancer Risk Evaluation

        ### Upload a mammogram and fill up the questionnaire, our model will evaluate the risk of breast cancer :computer:
        """
        )

        # Load the configuration file which stores the options for the questionnaire
        with open('src/options_config.json', 'r') as config_file:
            config = json.load(config_file)

        # Update patient_info dictionary based on user input
        self.patient_info["mammogram_image"] = st.file_uploader("Upload Mammogram Image", type=config['file_types'])

        # Display the uploaded image
        if self.patient_info["mammogram_image"] is not None:
            # Display the uploaded file directly
            st.image(self.patient_info["mammogram_image"], caption='Uploaded Image', width=300)

        # Conditional inputs for children and if user has had biopsy
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

        with st.form('my form', border= False):

            self.patient_info["age"] = st.slider("Age", **config['age_range'])
            self.patient_info["age_men"] = st.slider("Age of first Menstrual Period", **config['age_men_range'])
            self.patient_info["ethnicity"] = st.selectbox("Ethnicity", config['ethnicities'])
            self.patient_info["relatives_with_cancer"] = st.selectbox("Number of first degree relatives who had breast cancer", config['relatives_with_cancer'])
            self.patient_info["menopause_status"] = st.radio("Have you been through menopause?", config['menopause_status'])

            # Check for mammogram image upload
            if st.form_submit_button("Submit"):
                if self.patient_info["mammogram_image"] is None:
                    st.error("Please upload a mammogram if available")   
                else:
                    try:
                        birad_classification = self.model_controller.predict_birad_classification(self.patient_info["mammogram_image"])
                        self.patient_info["birad_classification"] = birad_classification
                    except Exception as e:
                        st.error(f"An error occurred trying to process the mammogram image, please check that the correct file was uploaded or try another mammogram if possible")

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
        '''This function generates an evaluation based on the risk_output by the model.'''

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
            st.write(f"Please upload a mammogram so our model can determine your Birad category, this will help to make a more informed analysis")

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
        st.markdown('''
        > ℹ️ **Note:** **Disclaimer: Important Limitations of Our Breast Cancer Risk Assessment Tool**
        >         
        > This risk assessment tool is not designed for individuals who have previously been diagnosed with breast cancer.
        The estimates and calculations provided by our tool are based on data from individuals who have not had a prior breast cancer diagnosis.
        If you have been diagnosed with breast cancer, we recommend seeking personalized advice and risk assessment from a healthcare professional.
        ?          
        > Our tool does not account for the increased risk associated with BRCA1 or BRCA2 gene mutations. Individuals with these genetic mutations 
        have a higher risk of developing breast cancer, which our assessment tool does not currently evaluate. If you are aware of carrying BRCA1
        or BRCA2 gene mutations, please consult with a genetic counselor or a medical professional for a more appropriate risk assessment.
        >         
        > The data used in our risk assessment model are exclusively sourced from patients from the United States. Therefore, the risk estimates may
        not be fully representative of individuals from other countries or with different ethnic backgrounds. The risk factors and their prevalence
        can vary significantly across different populations.
        >            
        > In our model, the incorporation of breast density as a risk factor is based on an estimation that utilizes the probability distribution of breast density. While breast density is a recognized factor in breast cancer risk, our method of incorporating it is an estimation as the original Gail Model does not include it as a factor. Therefore, our predictions should be interpreted with caution. 
        Please Note: The information provided by our Breast Cancer Risk Assessment Tool is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health providers with any questions you may have regarding a medical condition.
        ''')
