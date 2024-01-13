from src.UI.analysis_page import AnalysisPageInterface
import streamlit as st
from src.Model.ModelController import ModelController
from src.UI.home_page import HomePageInterface

def main():
    '''This function is the entry point for streamlit framework to compile and build the web app'''

    try:
        # Instantiate essential components of the app
        model_controller = ModelController()
        homepage = HomePageInterface()
        interface = AnalysisPageInterface(model_controller)
    except Exception as e:
        st.error(f"An error occured while loading the app components, please contact an administrator: {e}")

    # Implement navigation side bar
    st.sidebar.title("Main Menu :memo:")
    page = st.sidebar.selectbox("Choose a Page:", ["Home", "Analysis"])
        
    if page == "Analysis":
        interface.display()
    else:
        homepage.display()
    

if __name__ == "__main__":
    main()
