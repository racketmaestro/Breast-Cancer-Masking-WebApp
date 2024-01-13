
from src.patient_data import PatientData

def test_patient_data_initialization():
    patient = PatientData()
    assert patient.age is None
    assert patient.ethnicity is None
    assert patient.mammogram_image is None
