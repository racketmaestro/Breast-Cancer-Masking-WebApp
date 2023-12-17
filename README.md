# Breast Cancer Masking Web Application

### Setting up virtual environment

```pip install virtualenv```

Create the virtual environment: `virtualenv <your_venv_name>` 

Activate the virtual environment: `.\<your_venv_name>\Scripts\activate.bat` 

Install the dependencies in the virtual environment: ```pip install -r  requirements.txt```

Run the streamlit app for local development by entering `streamlit run app.py` in the command prompt

### Continuous Integration and Continuous Deployment

CI/CD pipeline was incorporated using Github Actions and Heroku

Github workflow set up to automatically build and run tests using pytest. This will be triggered through push or pull requests to 'master' branch. If tests are successful, it will be automatically deployed to Heroku platform, visible to the end user. 


