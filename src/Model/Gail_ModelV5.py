import numpy as np
import pandas as pd

class RiskModel:
    
    def __init__(self, data):
        # Assuming 'data' is a DataFrame with the necessary columns
        self.data = data

    def recode(self):
        # Accessing the data from the attribute
        data = self.data

        T1 = data.at[0, 'T1']
        biopCat = data.at[0, 'N_Biop']
        race = data.at[0, 'Race']
        ageMen = data.at[0, 'AgeMen']
        age1st = data.at[0, 'Age1st']
        nRels = data.at[0, 'N_Rels']
        hypPlas = data.at[0, 'HypPlas']
        biRads = data.at[0,'BiRads']
        menopause_status = data.at[0, 'menopause_status']
        
        menCat = np.nan
        birthCat = np.nan
        relativesCat = np.nan
        hypRiskScale = np.nan

        # Categorising menarchy age
        if (ageMen >= 14 and ageMen <= T1) or ageMen == 99: menCat = 0  
        elif ageMen >= 12 and ageMen < 14: menCat = 1
        elif ageMen > 7 and ageMen < 12: menCat = 2      

        if menCat == 2 and race == 2: menCat = 1 #  for African-Americans AgeMen code 2 (age <= 11) grouped with code 1(age == 12 or 13)

        # Categorising age of first birth
        if age1st < 20 or age1st == 99: birthCat = 0
        elif age1st >= 20 and age1st < 25: birthCat = 1
        elif (age1st >= 25 and age1st < 30) or age1st == 98: birthCat = 2
        elif age1st >= 30 and age1st < 98: birthCat = 3
        elif age1st > T1 and age1st < 98: birthCat = np.nan
        
        if race == 2: birthCat = 0 # for African-Americans Age1st is not a RR covariate and not in RR model, set to 0

        ## Categorising number of relatives with BRCA gene
        if nRels == 0 or nRels == 99: relativesCat = 0
        elif nRels == 1: relativesCat = 1
        elif nRels >= 2 and nRels < 99: relativesCat = 2
        
        if (race >= 6 and race <= 11) and relativesCat == 2: relativesCat = 1 # for Asians relativesCat = 2 is pooled with relativesCat = 1

        # Scaling by the risk of hyperplasia
        if biopCat == 0:
            hypRiskScale = 1.00
        elif biopCat > 0:
            if hypPlas == 0:
                hypRiskScale = 0.93
            elif hypPlas == 1:
                hypRiskScale = 1.82
            elif hypPlas == 99:
                hypRiskScale = 1.00
        
        ### hispanic RR model from San Francisco Bay Area Breast Cancer Study (SFBCS):
        ###         (1) groups N_Biop ge 2 with N_Biop eq 1
        ###         (2) eliminates  AgeMen from model for US Born hispanic women
        ###         (3) group Age1st=25-29 with Age1st=20-24 and code as 1
        ###             for   Age1st=30+, 98 (nulliparous)       code as 2
        ###         (4) groups N_Rels=2 with N_Rels=1;
        if biopCat == 99: biopCat = 0
        if race in [3,5] and biopCat in [0,99]: biopCat = 0
        if race in [3,5] and biopCat == 2: biopCat = 1
        if race == 3: menCat =0
        if race in [3,5] and age1st != 98 and birthCat == 2: birthCat = 1
        if race in [3,5] and birthCat == 3: birthCat = 2
        if race in [3,5] and relativesCat == 2: relativesCat = 1


        # race == 1 : "Wh"      white SEER 1983:87 BrCa Rate
        # race == 2 : "AA"      african-american
        # race == 3 : "HU"      hispanic-american (US born)
        # race == 4 : "NA"      other (native american and unknown race)
        # race == 5 : "HF"      hispanic-american (foreign born)
        # race == 6 : "Ch"      chinese
        # race == 7 : "Ja"      japanese
        # race == 8 : "Fi"      filipino
        # race == 9 : "Hw"      hawaiian
        # race == 10 : "oP"     other pacific islander
        # race == 11 : "oA"     other asian
            
        recodedData = pd.DataFrame({
            'T1': [T1],
            'biopCat': [biopCat],
            'menCat': [menCat],
            'birthCat': [birthCat],
            'relativesCat': [relativesCat],
            'hypRiskScale': [hypRiskScale],
            'race': [race],
            'biRads' : [biRads],
            'menopause_status' : [menopause_status],
        })
        
        return recodedData

    def relative_risk(self):
        data = self.data
        White_Beta = np.array([[0.3925, 0.0940103059, 
                                0.1885, 0.701, 
                                -0.2880424830, -0.1908113865]])
        Black_Beta = np.array([[0.1822121131, 0.2672530336, 
                                0.0, 0.4757242578, -0.1119411682, 0.0]])
        Hspnc_Beta = np.array([[0.0970783641, 0.0000000000, 
                                0.2318368334, 0.166685441, 
                                0.0000000000, 0.0000000000]])
        FHspnc_Beta = np.array([[0.4798624017, 0.2593922322, 
                                0.4669246218, 0.9076679727, 
                                0.0000000000, 0.0000000000]])
        Other_Beta = np.array([[0.5292641686, 0.0940103059, 
                                0.2186262218, 0.9583027845, 
                                -0.2880424830, -0.1908113865]])
        Asian_Beta = np.array([[0.55263612260619, 0.07499257592975, 
                                0.27638268294593, 0.79185633720481, 
                                0.0, 0.0]])
        Wrk_Beta_all = np.concatenate((White_Beta, Black_Beta, Hspnc_Beta, 
                                    Other_Beta, FHspnc_Beta, Asian_Beta, 
                                    Asian_Beta, Asian_Beta, Asian_Beta, 
                                    Asian_Beta, Asian_Beta))
        # Obtain covariates using recode_check function
        check_cov = self.recode()

        # Extract covariates
        biopCat= check_cov.at[0,'biopCat']
        menCat = check_cov.at[0,'menCat']
        birthCat = check_cov.at[0,'birthCat']
        relativesCat = check_cov.at[0,'relativesCat']
        hypRiskScale = check_cov.at[0,'hypRiskScale']
        race = check_cov.at[0,'race']
        

        # Select the appropriate beta coefficients
        Beta = Wrk_Beta_all[race-1]

        # Check if all covariates are available to calculate LP1 and LP2
        if not np.isnan(birthCat):
            LP1 = biopCat * Beta[0] + menCat * Beta[1] + birthCat * Beta[2] + relativesCat * Beta[3] + birthCat * relativesCat * Beta[5] + np.log(hypRiskScale)
            LP2 = LP1 + biopCat * Beta[4]
        else:
            LP1 = LP2 = np.nan

        # Calculate Relative Risks
        RR_Star1 = np.exp(LP1) if not np.isnan(LP1) else np.nan
        RR_Star2 = np.exp(LP2) if not np.isnan(LP2) else np.nan

        # Create a DataFrame for the result
        RR_Star = pd.DataFrame({'RR_Star1': [RR_Star1], 'RR_Star2': [RR_Star2]})

        return RR_Star

    def absolute_risk(self, lifetime):
        data = self.data
### set up lambda1*, lambda2, beta & F(t) with known constants used in the nci brca risk disk
    ## lambda1_Star, BrCa composite incidences
    # SEER BrCa incidence rates (current) non-hispanic white women, SEER white 1983:87
        White_lambda1 = np.array([[0.00001000, 0.00007600, 0.00026600, 0.00066100, 0.00126500, 0.00186600, 0.00221100, 
                        0.00272100, 0.00334800, 0.00392300, 0.00417800, 0.00443900, 0.00442100, 0.00410900]])
        # SEER BrCa incidence rates for "avg" non-hispanic white women and "avg" other (native american) women, SEER white 1992:96
        White_lambda1Avg = np.array([[0.00001220, 0.00007410, 0.00022970, 0.00056490, 0.00116450, 0.00195250, 0.00261540, 
                            0.00302790, 0.00367570, 0.00420290, 0.00473080, 0.00494250, 0.00479760, 0.00401060]])
        # SEER BrCa indicdence rates (under study) for non-hispanic white women, SEER white 1995:2003
        White_nlambda1 = np.array([[0.0000120469, 0.0000746893, 0.0002437767, 0.0005878291, 0.0012069622, 0.0019762053, 0.0026200977, 
                        0.0033401788, 0.0039743676, 0.0044875763, 0.0048945499, 0.0051610641, 0.0048268456, 0.0040407389]])
        # SEER black 1994-98
        Black_lambda1 = np.array([[0.00002696, 0.00011295, 0.00031094, 0.00067639, 0.00119444, 0.00187394, 0.00241504, 
                        0.00291112, 0.00310127, 0.00366560, 0.00393132, 0.00408951, 0.00396793, 0.00363712]])
        # SEER Ca Hisp 1995-2004
        Hspnc_lambda1 = np.array([[0.0000166, 0.0000741, 0.0002740, 0.0006099, 0.0012225, 0.0019027, 0.0023142, 
                        0.0028357, 0.0031144, 0.0030794, 0.0033344, 0.0035082, 0.0025308, 0.0020414]])
        # SEER white 1983:87
        Other_lambda1 = np.array([[0.00001000, 0.00007600, 0.00026600, 0.00066100, 0.00126500, 0.00186600, 0.00221100, 
                        0.00272100, 0.00334800, 0.00392300, 0.00417800, 0.00443900, 0.00442100, 0.00410900]])
        # SEER Ca Hisp 1995-2004
        FHspnc_lambda1 = np.array([[0.0000102, 0.0000531, 0.0001578, 0.0003602, 0.0007617, 0.0011599, 0.0014111,
                            0.0017245,  0.0020619, 0.0023603, 0.0025575, 0.0028227, 0.0028295, 0.0025868]])
        # seer18 chinese  1998:02
        Chnes_lambda1 = np.array([[0.000004059636, 0.000045944465, 0.000188279352, 0.000492930493, 0.000913603501,
                        0.001471537353, 0.001421275482, 0.001970946494, 0.001674745804, 0.001821581075,
                        0.001834477198, 0.001919911972, 0.002233371071, 0.002247315779]])
        # seer18 japanese 1998:02
        Japns_lambda1 = np.array([[0.000000000001, 0.000099483924, 0.000287041681, 0.000545285759, 0.001152211095,
                        0.001859245108, 0.002606291272, 0.003221751682, 0.004006961859, 0.003521715275,
                        0.003593038294, 0.003589303081, 0.003538507159, 0.002051572909]])
        # seer18 filipino 1998:02
        Filip_lambda1 = np.array([[0.000007500161, 0.000081073945, 0.000227492565, 0.000549786433, 0.001129400541,
                        0.001813873795, 0.002223665639, 0.002680309266, 0.002891219230, 0.002534421279,
                        0.002457159409, 0.002286616920, 0.001814802825, 0.001750879130]])
        # seer18 hawaiian 1998:02
        Hawai_lambda1 = np.array([[0.000045080582, 0.000098570724, 0.000339970860, 0.000852591429, 0.001668562761,
                        0.002552703284, 0.003321774046, 0.005373001776, 0.005237808549, 0.005581732512,
                        0.005677419355, 0.006513409962, 0.003889457523, 0.002949061662]])
        # seer18 otr pac isl 1998:02
        OtrPI_lambda1 = np.array([[0.000000000001, 0.000071525212, 0.000288799028, 0.000602250698, 0.000755579402,
                        0.000766406354, 0.001893124938, 0.002365580107, 0.002843933070, 0.002920921732,
                        0.002330395655, 0.002036291235, 0.001482683983, 0.001012248203]])
        # seer18 otr asian 1998:02
        OtrAs_lambda1 = np.array([[0.000012355409, 0.000059526456, 0.000184320831, 0.000454677273, 0.000791265338,
                        0.001048462801, 0.001372467817, 0.001495473711, 0.001646746198, 0.001478363563,
                        0.001216010125, 0.001067663700, 0.001376104012, 0.000661576644]])
        ## lambda2, Competing hazards
        #nchs competing mortality (current) for non-hispanic white women, NCHS white 1985:87
        White_lambda2 = np.array([[0.00049300, 0.00053100, 0.00062500, 0.00082500, 0.00130700, 0.00218100, 0.00365500, 
                        0.00585200, 0.00943900, 0.01502800, 0.02383900, 0.03883200, 0.06682800, 0.14490800]])
        # nchs competing mortality for "avg" non-hispanic white women and "avg" other (native american) women, NCHS white 1992:96
        White_lambda2Avg = np.array([[0.00044120, 0.00052540, 0.00067460, 0.00090920, 0.00125340, 0.00195700, 0.00329840, 
                            0.00546220, 0.00910350, 0.01418540, 0.02259350, 0.03611460, 0.06136260, 0.14206630]])
        # nchs competing mortality (under study) for non-hispanic white women, NCHS white 1995:2003
        White_nlambda2 = np.array([[0.0004000377, 0.0004280396, 0.0005656742, 0.0008474486, 0.0012752947, 0.0018601059, 0.0028780622, 
                            0.0046903348, 0.0078835252, 0.0127434461, 0.0208586233, 0.0335901145, 0.0575791439, 0.1377327125]])
        # NCHS black 1996-00
        Black_lambda2 = np.array([[0.00074354, 0.00101698, 0.00145937, 0.00215933, 0.00315077, 0.00448779, 0.00632281, 
                        0.00963037, 0.01471818, 0.02116304, 0.03266035, 0.04564087, 0.06835185, 0.13271262]])
        # SEER Ca Hisp 1995-2004
        Hspnc_lambda2 = np.array([[0.0003561, 0.0004038, 0.0005281, 0.0008875, 0.0013987, 0.0020769, 0.0030912,
                        0.0046960, 0.0076050, 0.0120555, 0.0193805, 0.0288386, 0.0429634, 0.0740349]])                
        # NCHS white 1985:87
        Other_lambda2 = np.array([[0.00049300, 0.00053100, 0.00062500, 0.00082500, 0.00130700, 0.00218100, 0.00365500, 
                        0.00585200, 0.00943900, 0.01502800, 0.02383900, 0.03883200, 0.06682800, 0.14490800]])
        # SEER Ca Hisp 1995-2004
        FHspnc_lambda2 = np.array([[0.0003129, 0.0002908, 0.0003515, 0.0004943, 0.0007807, 0.0012840, 0.0020325,
                            0.0034533, 0.0058674, 0.0096888, 0.0154429, 0.0254675, 0.0448037, 0.1125678]])
        # NCHS mortality chinese  1998:02
        Chnes_lambda2 = np.array([[0.000210649076, 0.000192644865, 0.000244435215, 0.000317895949, 0.000473261994,
                        0.000800271380, 0.001217480226, 0.002099836508, 0.003436889186, 0.006097405623,
                        0.010664526765, 0.020148678452, 0.037990796590, 0.098333900733]])
        # NCHS mortality japanese 1998:02
        Japns_lambda2 = np.array([[0.000173593803, 0.000295805882, 0.000228322534, 0.000363242389, 0.000590633044,
                        0.001086079485, 0.001859999966, 0.003216600974, 0.004719402141, 0.008535331402,
                        0.012433511681, 0.020230197885, 0.037725498348, 0.106149118663]])
        # NCHS mortality filipino 1998:02
        Filip_lambda2 = np.array([[0.000229120979, 0.000262988494, 0.000314844090, 0.000394471908, 0.000647622610,
                        0.001170202327, 0.001809380379, 0.002614170568, 0.004483330681, 0.007393665092,
                        0.012233059675, 0.021127058106, 0.037936954809, 0.085138518334]])
        # NCHS mortality hawaiian 1998:02
        Hawai_lambda2 = np.array([[0.000563507269, 0.000369640217, 0.001019912579, 0.001234013911, 0.002098344078,
                        0.002982934175, 0.005402445702, 0.009591474245, 0.016315472607, 0.020152229069,
                        0.027354838710, 0.050446998723, 0.072262026612, 0.145844504021]])
        # NCHS mortality otr pac isl 1998:02
        OtrPI_lambda2 = np.array([[0.000465500812, 0.000600466920, 0.000851057138, 0.001478265376, 0.001931486788,
                        0.003866623959, 0.004924932309, 0.008177071806, 0.008638202890, 0.018974658371,
                        0.029257567105, 0.038408980974, 0.052869579345, 0.074745721133]])
        # NCHS mortality otr asian 1998:02
        OtrAs_lambda2 = np.array([[0.000212632332, 0.000242170741, 0.000301552711, 0.000369053354, 0.000543002943,
                        0.000893862331, 0.001515172239, 0.002574669551, 0.004324370426, 0.007419621918,
                        0.013251765130, 0.022291427490, 0.041746550635, 0.087485802065]])
        # F(t), 1-Attributable Risk=F(t) 
        White_1_AR = np.array([[0.5788413, 0.5788413]])
        Black_1_AR = np.array([[0.72949880, 0.74397137]])
        Hspnc_1_AR = np.array([[0.749294788397, 0.778215491668]])
        Other_1_AR = np.array([[0.5788413, 0.5788413]])
        FHspnc_1_AR = np.array([[0.428864989813, 0.450352338746]])
        Asian_1_AR = np.array([[0.47519806426735, 0.50316401683903]])

        # initialize rate vectors with the correct rates for each woman under study based on her race
        # for i=1 to 11, when Race=i, Wrk_lambda1=Wrk_lambda1_all[i], Wrk_lambda2=Wrk_lambda2_all[i], Wrk_Beta=Wrk_Beta_all[i], Wrk_1_AR=Wrk_1_AR_all[i]
        Wrk_lambda1_all = np.concatenate((White_lambda1, Black_lambda1, Hspnc_lambda1, Other_lambda1, FHspnc_lambda1, Chnes_lambda1, Japns_lambda1, Filip_lambda1, Hawai_lambda1, OtrPI_lambda1, OtrAs_lambda1))
        Wrk_lambda2_all = np.concatenate((White_lambda2, Black_lambda2, Hspnc_lambda2, Other_lambda2, FHspnc_lambda2, Chnes_lambda2, Japns_lambda2, Filip_lambda2, Hawai_lambda2, OtrPI_lambda2, OtrAs_lambda2)) 
        Wrk_1_AR_all = np.concatenate((White_1_AR, Black_1_AR, Hspnc_1_AR, Other_1_AR, FHspnc_1_AR, Asian_1_AR, Asian_1_AR, Asian_1_AR, Asian_1_AR, Asian_1_AR, Asian_1_AR))
        
        # Recode data and calculate relative risk
        recoded_data = self.recode()
        rr_star = self.relative_risk()

        # Extract necessary information
        obs = recoded_data.iloc[0]
        race = int(obs['race'])
        T1 = obs['T1']
        biRads =obs['biRads']
        menopause_status = obs['menopause_status']
        if lifetime == 1:
            T2 = 90
        else:
            T2 = T1 + 5
        
        rrstar1 = rr_star['RR_Star1'].iloc[0]
        rrstar2 = rr_star['RR_Star2'].iloc[0]

        One_AR_RR = np.repeat(np.nan, 70) 

        One_AR1 = Wrk_1_AR_all[race-1,0]
        One_AR2 = Wrk_1_AR_all[race-1,1]

        # (1-AR)*RR at ages < 50
        One_AR_RR1 = One_AR1*rrstar1
        # (1-AR)*RR at ages >= 50
        One_AR_RR2 = One_AR2*rrstar2
        # define One_AR_RR
        One_AR_RR[0:30] = One_AR_RR1
        One_AR_RR[30:70] = One_AR_RR2

        # Compute Absolute Risk
        Strt_Intvl = int(np.floor(T1) - 20 + 1)
        End_Intvl = int(np.ceil(T2) - 20)
        NumbrIntvl = int(np.ceil(T2) - np.floor(T1))
        RskWrk = 0
        Cum_lambda = 0

        lambda1_temp = np.zeros((14, 5))
        lambda2_temp = np.zeros((14, 5))

        for v in range(lambda1_temp.shape[1]):
            lambda1_temp[:,v] = Wrk_lambda1_all[race-1,:]
            lambda2_temp[:,v] = Wrk_lambda2_all[race-1,:]
        lambda1 = lambda1_temp.flatten()
        lambda2 = lambda2_temp.flatten()

        for j in range(NumbrIntvl):
            j_intvl = Strt_Intvl+j-1
            if NumbrIntvl>1 and j>0 and j<NumbrIntvl-1:
                IntgrlLngth = 1

            if NumbrIntvl>1 and j==0:
                IntgrlLngth = 1-float((T1-np.floor(T1))) 
            if NumbrIntvl>1 and j+1==NumbrIntvl:
                z1 = np.where(T2>np.floor(T2), 1, 0)
                z2 = np.where(T2==np.floor(T2), 1, 0)
                IntgrlLngth = (float((T2-np.floor(T2)))*z1+z2)

            if NumbrIntvl==0:
                IntgrlLngth = (T2-T1)
            lambdaj = lambda1[j_intvl]*One_AR_RR[j_intvl]+lambda2[j_intvl]
                
            PI_j = ((One_AR_RR[j_intvl]*lambda1[j_intvl]/lambdaj)*np.exp(-Cum_lambda))*(1-np.exp(-lambdaj*IntgrlLngth))
            RskWrk = RskWrk+PI_j 
            Cum_lambda = Cum_lambda+lambdaj*IntgrlLngth

        AbsRisk = 100 * RskWrk

        # Probability distributions of BIRADS scores based on race (include source here)
        asian_BIRADS_dist_premenopause = [0.015, 0.172, 0.537, 0.275]
        asian_BIRADS_dist_postmenopause = [0.07, 0.382, 0.447, 0.101]
        white_BIRADS_dist_premenopause = [0.051, 0.326, 0.469, 0.144]
        white_BIRADS_dist_postmenopause = [0.130, 0.488, 0.331, 0.051]
        black_BIRADS_dist_premenopause = [0.065, 0.375, 0.462, 0.098]
        black_BIRADS_dist_postmenopause = [0.130, 0.548, 0.291, 0.030]
        hispanic_BIRADS_dist_premenopause = [0.069, 0.366, 0.454, 0.111]
        hispanic_BIRADS_dist_postmenopause = [0.172, 0.519, 0.272, 0.037]
        other_BIRADS_dist = [0.1587, 0.3413, 0.3413, 0.1587]
        BIRADS_risk_adjustment = 0

        if race == 1:
            if menopause_status:
                BIRADS_risk_adjustment = self.calculateRiskAdjustment(white_BIRADS_dist_postmenopause, biRads)

            else:
                BIRADS_risk_adjustment = self.calculateRiskAdjustment(white_BIRADS_dist_premenopause, biRads)

            
        elif race ==2:
            if menopause_status:
                BIRADS_risk_adjustment = self.calculateRiskAdjustment(black_BIRADS_dist_postmenopause, biRads)

            else:
                BIRADS_risk_adjustment = self.calculateRiskAdjustment(black_BIRADS_dist_premenopause, biRads)

        elif race == 4:
            BIRADS_risk_adjustment = self.calculateRiskAdjustment(other_BIRADS_dist, biRads)

        elif race in [3,5]:
            if menopause_status:
                BIRADS_risk_adjustment = self.calculateRiskAdjustment(hispanic_BIRADS_dist_postmenopause, biRads)

            else:
                BIRADS_risk_adjustment = self.calculateRiskAdjustment(hispanic_BIRADS_dist_premenopause, biRads)


        elif race in range(6,12):
            if menopause_status:
                BIRADS_risk_adjustment = self.calculateRiskAdjustment(asian_BIRADS_dist_postmenopause, biRads)

            else:
                BIRADS_risk_adjustment = self.calculateRiskAdjustment(asian_BIRADS_dist_premenopause, biRads)

        AbsRisk = AbsRisk * BIRADS_risk_adjustment


        
        return AbsRisk

    def calculateRiskAdjustment(self, dist, biRads_score):
        # Calculates the Weight Average Relative Risk (WARR) of each BIRADS distribution

        # BIRADS relative risks (RR) (include source here)
        BIRADS_RR_dict = { 
            "1.0": 0.5,
            "2.0" : 1,
            "3.0": 1.6,
            "4.0": 2.6
            }

        WARR = (dist[0]*BIRADS_RR_dict["1.0"]) + (dist[1]*BIRADS_RR_dict["2.0"]) + (dist[2]*BIRADS_RR_dict["3.0"]) + (dist[3]*BIRADS_RR_dict["4.0"])

        risk_adjustment = BIRADS_RR_dict[str(biRads_score)]/WARR

        return risk_adjustment

    def run_model(self):
        absRisk5 = self.absolute_risk(0)
        absRiskLifetime = self.absolute_risk(1)

        riskDict = {1: "Low", 2: "Medium", 3: "High"}

        riskIndex5 = np.ceil(absRisk5 / 100 * 3) if not np.isnan(absRisk5) else None
        riskIndexLifetime = np.ceil(absRiskLifetime / 100 * 3) if not np.isnan(absRiskLifetime) else None

        qualRisk5 = riskDict.get(riskIndex5, "Unknown")
        qualRiskLife = riskDict.get(riskIndexLifetime, "Unknown")

        riskDict = {
            "5 Year risk figure": absRisk5, 
            "Lifetime risk figure": absRiskLifetime, 
            "Qualitative 5 year risk": qualRisk5, 
            "Qualitative lifetime risk": qualRiskLife
        }
        return riskDict


