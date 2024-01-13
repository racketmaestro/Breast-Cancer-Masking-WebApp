
# Breast Cancer Masking Web Application

## Project Summary

This project aims to provide an accessible platform for users to receive a quick breast cancer risk assessment based on their health data and mammograms. 

Risk of breast cancer is known to increase with breast density. However, the current online Breast Cancer Risk Assessment Tool (BCRAT), also known as the [Gail Model](https://bcrisktool.cancer.gov/), only uses select health data to make a quick risk analysis. 

Our risk prediction model extends the Gail Model by incorporating breast density and menopause data, which are factors that affect the risk of breast cancer, to make a more informed risk assessment.

Breast density is determined by running the mammogram through a Convolutional Neural Network Tensorflow model that is trained on the [Mini-DDSM Dataset](https://www.kaggle.com/datasets/cheddad/miniddsm2). The model outputs the probability density function for BI-RADS categories (A, B, C and D). Users or doctors with an available mammogram can easily upload it and fill in the questionnaire on the web app.

Refer to the web app to find out more about the technical details behind our models.

[Streamlit](https://streamlit.io/) library was used to construct the user interface. 

[Check out the web app here!](https://breast-cancer-masking-webapp-7bdeafc2e921.herokuapp.com/)

## Setting up a virtual environment

You can use your preferred way to set up the virtual environment.

```pip install virtualenv```

Create the virtual environment: `virtualenv <your_venv_name>` 

Activate the virtual environment: `.\<your_venv_name>\Scripts\activate.bat` 

Install the dependencies in the virtual environment: ```pip install -r  requirements.txt```


## Local development

Run the streamlit app for local development by running `streamlit run app.py` in the command prompt. Make changes on the dev branch before merging to the master branch.

Run tests using the command `pytest` in the root directory. Test cases can be found in the'tests' folder.

## Continuous Integration and Continuous Deployment

CI/CD pipeline was incorporated using Github Actions and Heroku

**Trigger Activation:**

Triggered on push or pull requests to the master branch.

**Build and Test** (refer to python-app.yml)

- Environment: Runs on the latest Ubuntu runner.
- Python Setup: Uses Python 3.10.
- Dependencies: Installs from requirements.txt and essential tools.
- Linting: Code quality checked with flake8.
- Testing: Runs tests using pytest. (test cases in found in 'tests' folder)

**Deployment**

- Heroku Deployment: On successful build and test, the app is deployed to Heroku.
- Conditions: Deployment occurs only if the commit is on master and all tests pass.
- If any test cases fail or errors in code, stop the merge into master and prevent deployment to Heroku.

**Best Practices**

- Security: Credentials securely stored in GitHub secrets which is only visible to admins of the repository.
- Efficiency: Pipeline ensures code quality and functionality before deployment to Heroku platform.
- This pipeline facilitates a development workflow, ensuring reliability, availability, and quality of code in the production environment.


## Contributors

- [Amos Koh](https://github.com/racketmaestro)
- [Aveek Goswami](https://github.com/magichampz)
- [Cameron Briginshaw](https://github.com/CptCold12)
- [Low Wei Han](https://github.com/weihanlow)
- [David Silcock](https://github.com/dsilcock03)

As part of Bioengineering Department in Imperial College London
