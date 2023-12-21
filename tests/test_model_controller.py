from src.Model.ModelController import ModelController
import pytest

@pytest.fixture
def model_controller():
    return ModelController()

def test_init(model_controller):
    """
    Test if the model is loaded successfully.
    """
    assert model_controller.cancer_detection_model is not None, "Model should be loaded"

def test_predict_cancer(model_controller):
    """
    Test the predict_cancer function with a mock image file.
    """
    # Create a mock image file
    from PIL import Image
    import io

    # Create a simple black square image
    img = Image.new('L', (128, 128), color = 'black')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = io.BytesIO(img_byte_arr.getvalue())

    # Test the predict_cancer function
    prediction = model_controller.predict_cancer(img_byte_arr)
    assert prediction is not None, "predict_cancer should return a prediction"


