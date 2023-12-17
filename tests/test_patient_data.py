
from src.patient_data import PatientData

def test_patient_data_initialization():
    patient = PatientData()
    assert patient.age is None
    assert patient.ethnicity is None
    assert patient.smoker is None
    assert patient.country is None
    assert patient.mammogram_image is None


def test_get_data_summary():
    patient = PatientData()
    patient.set_data(45, "Caucasian", False, "USA", None)
    summary = patient.get_data_summary()
    assert summary == {
        "Age": 45,
        "Ethnicity": "Caucasian",
        "Smoker": False,
        "Country": "USA",
        "Mammogram Image": "Not Uploaded"
    }
