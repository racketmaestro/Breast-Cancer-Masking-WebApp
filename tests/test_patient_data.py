
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
    patient.set_data(age=30, ageMen=13, ethnicity="Caucasian", relativesWithCancer=1, 
                     ageAtFirstChild=25, numBenignDiagnoses='1', 
                     atypicalHyperplasiaStatus='No', mammogram_image=None)
    
    # Expected summary
    expected_summary = {
        "Age": 30,
        "Agemen": 13,
        "Ethnicity": "Caucasian",
        "Relatives with cancer": 1,
        "Age at first child": 25,
        "Number of benign diagnoses": '1',
        "Atypical Hyperplasia Status": 'No',
        "Mammogram Image": "Not Uploaded"
    }

    # Call get_data_summary
    summary = patient.get_data_summary()

    # Assert that the returned summary matches the expected summary
    assert summary == expected_summary
