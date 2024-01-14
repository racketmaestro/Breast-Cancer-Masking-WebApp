import streamlit as st


class HomePageInterface:
    """
    This class handles the display and components of the Home Page of the web app
    """

    def __init__(self):
        pass

    def display(self):
        # Create the UI components
        left_col, right_col = st.columns(2)

        left_col.markdown("# Dilcock Health")
        left_col.markdown("## A tool for analyzing risk of breast cancer")
        left_col.markdown("*Created by Silcock and Sons*")

        # URL of the image
        image_url = (
            "https://cdn.pixabay.com/photo/2021/11/20/03/16/doctor-6810750_1280.png"
        )

        # Display the image in the right column
        right_col.image(image_url, caption="Your friendly online helper")

        st.markdown(
            """
        ---
        ## Summary

        This project aims to provide an accessible platform for users to receive a quick breast cancer risk assessment based on their health data and mammograms. 
        Risk of breast cancer is known to increase with breast density. However, the current online Breast Cancer Risk Assessment Tool (BCRAT), also known as the Gail Model, only uses select health data to make a quick risk analysis.

        Our risk prediction model extends the Gail Model by incorporating breast density and menopause data, which are factors that affect the risk of breast cancer, to make a more informed risk assessment.

        Breast density is determined by running the mammogram through a Convolutional Neural Network Tensorflow model that is trained on the Mini-DDSM Dataset. The model outputs the probability density function for Breast Imaging Reporting and Data System (BI-RADS) categories (A, B, C and D). Users or doctors with an available mammogram can easily upload it and fill in the questionnaire on the web app.

        """
        )

        # Function to read the contents of the text file
        def load_markdown_file(markdown_file):
            with open(markdown_file, "r", encoding="utf-8") as file:
                return file.read()

        markdown_file_path = "src/UI/homepage_writeup.txt"

        # Load and display the content as Markdown
        markdown_content = load_markdown_file(markdown_file_path)
        st.markdown(markdown_content, unsafe_allow_html=True)

        st.markdown("### Image Processing Pipeline Demonstration")

        st.image("src/UI/images/processing.png")

        st.markdown(
        """
        ---
        ### Contributors
        
        - [Amos Koh](https://www.linkedin.com/in/ak726/)
        - [Aveek Goswami](https://www.linkedin.com/in/aveekg00/)
        - [Cameron Briginshaw](https://www.linkedin.com/in/cb1409/)
        - [Low Wei Han](https://www.linkedin.com/in/whl720/)
        - [David Silcock](https://www.linkedin.com/in/david-silcock-482674297/)
                    
        [![Source Code](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/racketmaestro/Breast-Cancer-Masking-WebApp)
        """
        )
