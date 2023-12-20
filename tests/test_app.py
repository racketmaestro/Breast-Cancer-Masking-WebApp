from streamlit.testing.v1 import AppTest

def test_app():
    '''This uses the streamlit AppTest api to simulate a running app'''
    at = AppTest.from_file("app.py")
    at.run(timeout = 30)
    assert not at.exception 
