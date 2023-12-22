from src.UI.patient_interface import PatientInputInterface
import streamlit as st
from src.Model.ModelController import ModelController
from src.UI.home_page import HomePageInterface

def main():

    try:
        model_controller = ModelController()
        homepage = HomePageInterface()
        interface = PatientInputInterface(model_controller)
    except Exception as e:
        st.error(f"An error occured while loading the page, please contact an administrator: {e}")

    st.sidebar.title("Main Menu")
    page = st.sidebar.selectbox("Choose a Page:", ["Home", "Analysis"])

    if page == "Analysis":
        interface.display()
    else:
        homepage.display()
    

if __name__ == "__main__":
    main()
