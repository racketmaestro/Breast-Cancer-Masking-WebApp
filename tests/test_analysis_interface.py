import pytest
from src.Model.ModelController import ModelController
from src.UI.analysis_page import AnalysisPageInterface
from src.patient_data import PatientData

def test_initialization():
    model_controller = ModelController()
    api = AnalysisPageInterface(model_controller)
    assert api.model_controller == model_controller
    assert isinstance(api.patient_data, PatientData)
    assert isinstance(api.patient_info, dict)
