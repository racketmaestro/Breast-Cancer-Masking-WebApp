from src.UI.patient_interface import PatientInputInterface
import streamlit as st


def main():
    interface = PatientInputInterface()
    
    # Load the web app user interface
    try:
        interface.display()
    except Exception as e:
        st.error(f"An error occured while loading the page: {e}")

if __name__ == "__main__":
    main()
