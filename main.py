# 1. Organize the data by creating cvs files for each condition (cold,cool,warm,heat) with only data on Heart Rate for each participant 
# I have saved a cvs file for each participant, now I want to create cvs file, one for each thermal condition. In this new cvs file, each sheet has data for one participant. 
# In each the first column is the time, the second column the value of HR and in the third column there should be a numerical code : 1 all the data in the block 1, 2 all the data in the block 2 and so on untill block 5 

import pandas as pd

#The cvs file for each participants

name_cvs_mild = ['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13','P14','P15','P16','P17','P18','P19','P20','P21','P22','P23','P24','P25','P26']
name_cvs_extreme = ['P2','P3', 'P5','P6','P7','P9','P10','P11','P12','P13','P14','P15','P16','P18','P19','P20','P21','P22','P23','P24','P25','P26','P27','P28','P29'] 

#folder which all the file are saved on my PC 
directory_mild = "/Users/margheritabisaglia/Library/CloudStorage/OneDrive-ScientificNetworkSouthTyrol/UniTN/TESI tXc/EXP_thp/EXP_tirocinante_1/"
directory_extreme = "/Users/margheritabisaglia/Library/CloudStorage/OneDrive-ScientificNetworkSouthTyrol/UniTN/TESI tXc/EXP_SPRING24/PARTECIPANTI/"



## COOL AND COLD TEMPERATURES 
#loop trough all the participant 

HR_cool_dict = {}
for participant in name_cvs_mild:
     file_path_cool = f"{directory_mild}{participant}.xlsx" 
     file_cool=pd.read_excel(file_path_cool,sheet_name="Eq_cold")
     HR_cool =pd.DataFrame({'time':file_cool["Time (HH:mm:ss)"],'HR':file_cool['HR (bpm)']})
     HR_cool_dict[participant] = HR_cool

HR_cold_dict = {}
for participant in name_cvs_extreme:  
        file_path_cold= f"{directory_extreme}{participant}.xlsx"  
        file_cold=pd.read_excel(file_path_cold, sheet_name="Eq_cold")
        HR_cold =pd.DataFrame({'time':file_cold["Time (HH:mm:ss)"],'HR':file_cold['HR (bpm)']})
        HR_cold_dict[participant] = HR_cold
 
print(HR_cool_dict["P1"].head())   # shows first rows for P1
print(HR_cool_dict["P2"].head()) 



