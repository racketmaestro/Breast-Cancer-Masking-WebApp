# Breast Cancer Masking Web Application

## Project Summary


[Website](https://breast-cancer-masking-webapp-7bdeafc2e921.herokuapp.com/)

## Development

## Setting up virtual environment

```pip install virtualenv```

Create the virtual environment: `virtualenv <your_venv_name>` 

Activate the virtual environment: `.\<your_venv_name>\Scripts\activate.bat` 

Install the dependencies in the virtual environment: ```pip install -r  requirements.txt```


## Local development

Run the streamlit app for local development by entering `streamlit run app.py` in the command prompt. Make changes on the dev branch before merging to the master branch.

Run tests using the command `pytest` in the root directory. 


## Continuous Integration and Continuous Deployment

CI/CD pipeline was incorporated using Github Actions and Heroku

Github workflow set up to automatically build and run tests (pytest) and check code quality (pylint). This will be triggered through push or merge requests to 'master' branch. If tests are successful, Github Actions will deploy the web application to Heroku platform, the production platform that is visible to end users. 




