import streamlit as st

class ResultsInterface():
    
    def __init__(self, prediction):
        self.prediction = prediction
        pass

    def generate_diagnosis_display(self):
        if self.prediction[0][1] > 0.8:
            st.markdown('##Our model indicates that your mammogram has signs of tumour growth')
        else:
            st.markdown('##Our model indicates that your mammogram has no signs of tumour growth')

        pass
    
    def generate_feedback():
        st.markdown('##Based on the information provided, our model has the following risk assessment')
        st.markdown('---')
        st.write(f'Our model indicates that you have a Bi-rad classification of class')
        pass

    def generate_graph():
        pass

    def display():
        pass

