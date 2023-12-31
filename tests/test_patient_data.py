
from src.patient_data import PatientData

def test_patient_data_initialization():
    patient = PatientData()
    assert patient.age is None
    assert patient.ethnicity is None
    assert patient.mammogram_image is None


def test_get_data_summary():
    # Create an instance of the PatientData class
    patient = PatientData()

    # Set some data for the patient
    patient.set_data(age=30, age_men=13, ethnicity="Chinese", relatives_with_cancer="One", 
                     age_at_first_child=25, num_benign_diagnoses="One", 
                     atypical_hyperplasia_status="No", mammogram_image=None)
    
    # Expected summary
    expected_summary = {
        "Age": 30,
        "Agemen": 13,
        "Ethnicity": "Chinese",
        "Relatives with cancer": "One",
        "Age at first child": 25,
        "Number of benign diagnoses": "One",
        "Atypical Hyperplasia Status": "No",
        "Mammogram Image": "Not Uploaded"
    }

    # Call get_data_summary
    summary = patient.get_data_summary()

    # Assert that the returned summary matches the expected summary
    assert summary == expected_summary
