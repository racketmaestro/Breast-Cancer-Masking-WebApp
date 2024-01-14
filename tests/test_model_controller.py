from src.Model.model_controller import ModelController
import pytest

@pytest.fixture
def model_controller():
    return ModelController()

def test_init(model_controller):
    """
    Test if the model is loaded successfully.
    """
    assert model_controller.birad_classification_model is not None, "Model should be loaded"

