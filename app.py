from src.UI.patient_interface import PatientInputInterface
import streamlit as st
from src.Model.ModelController import ModelController

def main():

    try:
        # Load the web app user interface
        interface = PatientInputInterface()
        interface.display()
    except Exception as e:
        st.error(f"An error occured while loading the page, please contact an administrator: {e}")

    model_controller = ModelController()
    

if __name__ == "__main__":
    main()
