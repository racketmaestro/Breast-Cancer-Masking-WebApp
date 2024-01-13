import streamlit as st

class HomePageInterface():
    '''
    This class handles the display and components of the Home Page of the web app
    '''
    def __init__(self):
        pass

    def display(self):

        # Create the UI components
        left_col, right_col = st.columns(2)

        left_col.markdown("# Dilcock Health")
        left_col.markdown("### A tool for analyzing risk of breast cancer")
        left_col.markdown("**Created by Silcock and Sons**")
        left_col.markdown("**Amos Koh, Cameron Briginshaw, Aveek Goswami, Wei Han Low, David Silcock**")

        # URL of the image
        image_url ='https://cdn.pixabay.com/photo/2020/05/25/03/37/doctor-5216835_1280.png'

        # Display the image in the right column
        right_col.image(image_url, caption='Mr Dilcock will see you now')


        st.markdown(
        """
        ---
        ### Summary

        *Dilcocks rule*

        """
        )
