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
        left_col.markdown("## A tool for analyzing risk of breast cancer")
        left_col.markdown("*Created by Silcock and Sons*")

        # URL of the image
        image_url ='https://cdn.pixabay.com/photo/2021/11/20/03/16/doctor-6810750_1280.png'

        # Display the image in the right column
        right_col.image(image_url, caption='Your friendly online helper')

        st.markdown(
        """
        ---
        ## Summary

        *Dilcocks rule*

        ---
        """
        )

        st.markdown("""
        ### Contributors
        
        - [Amos Koh](https://www.linkedin.com/in/ak726/)
        - [Aveek Goswami](https://www.linkedin.com/in/aveekg00/)
        - [Cameron Briginshaw](https://www.linkedin.com/in/cb1409/)
        - [Low Wei Han](https://www.linkedin.com/in/whl720/)
        - [David Silcock](https://www.linkedin.com/in/david-silcock-482674297/)
                    
        [![Source Code](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/racketmaestro/Breast-Cancer-Masking-WebApp)
        """)