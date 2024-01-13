
# Breast Cancer Masking Web Application

## Project Summary

This project aims to 

[Website](https://breast-cancer-masking-webapp-7bdeafc2e921.herokuapp.com/)

## Setting up virtual environment

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
- If any test cases fail or errors in code, stop the merge into master and prevent deployment eployment to Heroku.

**Best Practices**

- Security: Credentials securely stored in GitHub secrets which is only visible to admins of the repository.
- Efficiency: Pipeline ensures code quality and functionality before deployment to Heroku platform.
- This pipeline facilitates a development workflow, ensuring reliability, availability, and quality of code in the production environment.


### Contributors

- [Amos Koh](https://github.com/racketmaestro)
- [Aveek Goswami](https://github.com/magichampz)
- [Cameron Briginshaw](https://github.com/CptCold12)
- [Low Wei Han](https://github.com/weihanlow)
- [David Silcock](https://github.com/dsilcock03)

As part of Bioengineering Department in Imperial College London
