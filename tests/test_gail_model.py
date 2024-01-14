import numpy as np
import pandas as pd
from src.Model.risk_model import RiskModel

def test_gail_model():
    '''This unit test will generate synthetic data using DataSynthesizer for the gail model and
      check that the quantitative risk assessment does not exceed 100%'''
    
    data_synth = DataSynthesizer()

    # Generate sets of user data and test them
    for i in range(10):
        data_dict = data_synth.data_gen()
        data = pd.DataFrame([data_dict])
        risk_model = RiskModel(data)
        riskDict = risk_model.run_model()

        assert riskDict["5 Year risk figure"]<100 and riskDict["Lifetime risk figure"]<100, "Gail model computations should output percentage less than 100"

class DataSynthesizer: 
    '''This class generates the synthetic data'''

    def data_synth_norm(self):

        # Define mean and standard deviation for T1, ageMen, and age1st
        T1_mean, T1_std = 60, 10
        ageMen_mean, ageMen_std = 12, 1.5
        age1st_mean, age1st_std = 24, 3

        # Generate normally distributed data and apply constraints
        T1 = min(max(int(np.random.normal(T1_mean, T1_std)), 35), 85)
        AgeMen = min(max(int(np.random.normal(ageMen_mean, ageMen_std)), 7), 15)
        
        # Ensure age1st is between 15 and T1 or 98
        has_children = np.random.choice([True, False])

        if has_children:
            # Generate normally distributed age between 15 and T1
            Age1st = min(max(int(np.random.normal(age1st_mean, age1st_std)), 15), T1)
        else:
            # Assign 98 to represent no children
            Age1st = 98

        # Categorical parameters are sampled from their respective categories
        N_Biop = np.random.choice([0, 1, 2, 99])
        Race = np.random.choice(range(1, 12))
        N_Rels = np.random.choice([0, 1, 2, 99])
        HypPlas = np.random.choice([0, 1, 99])
        BiRads = np.random.choice(range(1, 5))
        menopause_status = np.random.choice([0, 1])

        # Create and return the dictionary
        return {
            'T1': T1,
            'N_Biop': N_Biop,
            'Race': Race,
            'AgeMen': AgeMen,
            'Age1st': Age1st,
            'N_Rels': N_Rels,
            'HypPlas': HypPlas,
            'BiRads': BiRads,
            'menopause_status': menopause_status
        }

    def convert_numpy_int_to_python_int(self, data):
        for key, value in data.items():
            if isinstance(value, np.integer):
                data[key] = int(value)
        return data

    def data_gen(self):
        # Generate the data
        data_dict = self.data_synth_norm()

        # Convert NumPy integers to Python integers
        data_dict = self.convert_numpy_int_to_python_int(data_dict)

        return data_dict