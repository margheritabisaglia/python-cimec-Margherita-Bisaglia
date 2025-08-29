
# ============================================================
# DATA ORGANIZATION
# ============================================================
# 1. For each thermal condition (Cold, Cool, Warm, Hot), 
#    create a single Excel file that contains HR data from all participants.  
#
# 2. Input: individual Excel files already saved for each participant.  
#
# 3. Output: one Excel file per condition (e.g., HR_cool_all.xlsx), 
#    where each sheet corresponds to one participant.  
#
# 4. Structure of each sheet:
#      - Column 1: Time  
#      - Column 2: Heart Rate (HR)  
#      - Column 3: Block number (1–5), assigned according to time intervals.  
#
# 5. Block labeling:  
#      - Block 1 → all rows belonging to time range 1  
#      - Block 2 → all rows belonging to time range 2  
#      - … until Block 5.

import pandas as pd 
from datetime import datetime

# List of participant IDs (mild condition group)
name_cvs_mild = ['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10',
                 'P11','P12','P13','P14','P15','P16','P17','P18','P19','P20',
                 'P21','P22','P23','P24','P25','P26']

# List of participant IDs (extreme condition group)
name_cvs_extreme = ['P2','P3','P5','P6','P7','P9','P10','P11','P12','P13',
                    'P14','P15','P16','P18','P19','P20','P21','P22','P23','P24',
                    'P25','P26','P27','P28','P29'] 

# Directories where participant Excel files are stored
directory_mild = "/Users/margheritabisaglia/Library/CloudStorage/OneDrive-ScientificNetworkSouthTyrol/UniTN/TESI tXc/EXP_thp/EXP_tirocinante_1/"
directory_extreme = "/Users/margheritabisaglia/Library/CloudStorage/OneDrive-ScientificNetworkSouthTyrol/UniTN/TESI tXc/EXP_SPRING24/PARTECIPANTI/"

# ============================================================
# COOL condition (18 °C)
# ============================================================

HR_cool_dict = {}
# Define block start/end indices (time intervals for 5 blocks)
blocks_boundaries = { "b1": (2, 29), "b2": (31, 58),"b3": (60, 87),"b4": (89, 91),"b5": (118, 147)}

for participant in name_cvs_mild:
     file_path_cool = f"{directory_mild}{participant}.xlsx" 

     # Skip if required sheets ("Cold" and "Eq_cold") are missing
     sheet_names = pd.ExcelFile(file_path_cool).sheet_names
     if not {"Cold", "Eq_cold"}.issubset(sheet_names):
         continue
     
     # Extract start/end times for each block from "Cold" sheet
     file_cool_time_info=pd.read_excel(file_path_cool, sheet_name="Cold") 
     file_cool_time_info = file_cool_time_info["Unnamed: 2"]

     block_dict = {}
     for name, (start, end) in blocks_boundaries.items():
         start_time = file_cool_time_info[start]    
         end_time   = file_cool_time_info[end]      
         block_dict[name] = [start_time, end_time]

     # Read HR data from "Eq_cold" sheet
     file_cool_HR_info=pd.read_excel(file_path_cool,sheet_name="Eq_cold")

     # Skip if HR sheet is empty 
     if file_cool_HR_info.empty or not {"Time (HH:mm:ss)", "HR (bpm)"}.issubset(file_cool_HR_info.columns):
         continue
     
     # Build dataframe with time, HR, and block labels
     HR_cool = pd.DataFrame({
         'time': file_cool_HR_info["Time (HH:mm:ss)"],
         'HR': file_cool_HR_info['HR (bpm)']
     })
     HR_cool["block"] = 0
     
     # Assign block number based on time ranges
     for i, (name, (start, end)) in enumerate(block_dict.items(), start=1):
         mask = (HR_cool["time"] >= start) & (HR_cool["time"] <= end)
         HR_cool.loc[mask, "block"] = i
         HR_cool_dict[participant] = HR_cool

# Preview check
print(HR_cool_dict["P1"].head()) 

# Save all participants (sheets) into one Excel file
writer = pd.ExcelWriter("/Users/margheritabisaglia/Library/CloudStorage/OneDrive-ScientificNetworkSouthTyrol/PhD/Courses/Python 2025/HR_cool_all.xlsx")
for name, df in HR_cool_dict.items():
    df.to_excel(writer, sheet_name=name)
writer.close()
     

# ============================================================
# COLD condition 
# ============================================================

HR_cold_dict = {}
blocks_boundaries = { "b1": (3, 31), "b2": (33, 61),"b3": (63, 91),"b4": (95, 123),"b5": (125, 152)}

for participant in name_cvs_extreme:
     print(participant)
     file_path_cold = f"{directory_extreme}{participant}.xlsx" 

     # Skip if required sheets ("Warm" and "Eq_warm") are missing
     sheet_names = pd.ExcelFile(file_path_cold).sheet_names
     if not {"Warm", "Eq_warm"}.issubset(sheet_names):
         continue

     # Extract block start/end times from "Warm" sheet
     file_cold_time_info=pd.read_excel(file_path_cold, sheet_name="Cold") 
     file_cold_time_info = file_cold_time_info["Unnamed: 3"]

     block_dict = {}
     for name, (start, end) in blocks_boundaries.items():
         start_time = file_cold_time_info[start]    
         end_time   = file_cold_time_info[end]      
         block_dict[name] = [start_time, end_time]

     # Read HR data from "Eq_warm"
     file_cold_HR_info=pd.read_excel(file_path_cold,sheet_name="Eq_cold")

     # Skip if HR sheet is empty or missing columns
     if file_cold_HR_info.empty or not {"Time (HH:mm:ss)", "HR (bpm)"}.issubset(file_cold_HR_info.columns):
         continue

     # Build dataframe with time, HR, and block labels
     HR_cold = pd.DataFrame({
         'time': file_cold_HR_info["Time (HH:mm:ss)"],
         'HR': file_cold_HR_info['HR (bpm)']
     })
     HR_cold["block"] = 0

     # filter out non string values
     HR_cold["time"] = HR_cold["time"].apply(lambda x: x if isinstance(x, str) else None)
     
     # Assign block numbers
     for i, (name, (start, end)) in enumerate(block_dict.items(), start=1):
         mask = (HR_cold["time"] >= start) & (HR_cold["time"] <= end)
         HR_cold.loc[mask, "block"] = i
         HR_cold_dict[participant] = HR_cold

# Preview check
print(HR_cold_dict["P2"].head())

# Save combined Excel
writer = pd.ExcelWriter("/Users/margheritabisaglia/Library/CloudStorage/OneDrive-ScientificNetworkSouthTyrol/PhD/Courses/Python 2025/HR_cold_all.xlsx") 
for name, df in HR_cold_dict.items():
    df.to_excel(writer, sheet_name=name)
writer.close() 


# ============================================================
# WARM condition 
# ============================================================

HR_warm_dict = {}
blocks_boundaries = { "b1": (2, 29), "b2": (31, 58),"b3": (60, 87),"b4": (89, 91),"b5": (118, 147)}

for participant in name_cvs_mild:
     file_path_warm = f"{directory_mild}{participant}.xlsx" 

     # Skip if required sheets ("Warm" and "Eq_warm") are missing
     sheet_names = pd.ExcelFile(file_path_warm).sheet_names
     if not {"Warm", "Eq_warm"}.issubset(sheet_names):
         continue
     
     # Extract block start/end times from "Warm" sheet
     file_warm_time_info=pd.read_excel(file_path_warm, sheet_name="Warm") 
     file_warm_time_info = file_warm_time_info["Unnamed: 2"]

     block_dict = {}
     for name, (start, end) in blocks_boundaries.items():
         start_time = file_warm_time_info[start]    
         end_time   = file_warm_time_info[end]      
         block_dict[name] = [start_time, end_time]

     # Read HR data
     file_warm_HR_info=pd.read_excel(file_path_warm,sheet_name="Eq_warm")

     # Skip if HR sheet is empty or missing columns
     if file_warm_HR_info.empty or not {"Time (HH:mm:ss)", "HR (bpm)"}.issubset(file_warm_HR_info.columns):
         continue

     # Build dataframe
     HR_warm = pd.DataFrame({
         'time': file_warm_HR_info["Time (HH:mm:ss)"],
         'HR': file_warm_HR_info['HR (bpm)']
     })
     HR_warm["block"] = 0
     
     # Assign block numbers
     for i, (name, (start, end)) in enumerate(block_dict.items(), start=1):
         mask = (HR_warm["time"] >= start) & (HR_warm["time"] <= end)
         HR_warm.loc[mask, "block"] = i
         HR_warm_dict[participant] = HR_warm

# Preview check
print(HR_warm_dict["P1"].head()) 

# Save combined Excel
writer = pd.ExcelWriter("/Users/margheritabisaglia/Library/CloudStorage/OneDrive-ScientificNetworkSouthTyrol/PhD/Courses/Python 2025/HR_warm_all.xlsx") 
for name, df in HR_warm_dict.items():
    df.to_excel(writer, sheet_name=name)
writer.close()


# ============================================================
# HOT condition 
# ============================================================

HR_hot_dict = {}
blocks_boundaries = { "b1": (3, 31), "b2": (33, 61),"b3": (63, 91),"b4": (95, 123),"b5": (125, 152)}

for participant in name_cvs_extreme:
     file_path_hot = f"{directory_extreme}{participant}.xlsx" 

     # Skip if required sheets ("Warm" and "Eq_warm") are missing
     sheet_names = pd.ExcelFile(file_path_hot).sheet_names
     if not {"Warm", "Eq_warm"}.issubset(sheet_names):
         continue

     # Extract block start/end times from "Warm" sheet
     file_hot_time_info=pd.read_excel(file_path_hot, sheet_name="Warm") 
     file_hot_time_info = file_hot_time_info["Unnamed: 3"]

     block_dict = {}
     for name, (start, end) in blocks_boundaries.items():
         start_time = file_hot_time_info[start]    
         end_time   = file_hot_time_info[end]      
         block_dict[name] = [start_time, end_time]

     # Read HR data
     file_hot_HR_info=pd.read_excel(file_path_hot,sheet_name="Eq_warm")

     # Skip if HR sheet is empty or missing columns
     if file_hot_HR_info.empty or not {"Time (HH:mm:ss)", "HR (bpm)"}.issubset(file_hot_HR_info.columns):
         continue

     # Build dataframe
     HR_hot = pd.DataFrame({
         'time': file_hot_HR_info["Time (HH:mm:ss)"],
         'HR': file_hot_HR_info['HR (bpm)']
     })
     HR_hot["block"] = 0
     
     # Assign block numbers
     for i, (name, (start, end)) in enumerate(block_dict.items(), start=1):
         mask = (HR_hot["time"] >= start) & (HR_hot["time"] <= end)
         HR_hot.loc[mask, "block"] = i
         HR_hot_dict[participant] = HR_hot

# Preview check
print(HR_hot_dict["P2"].head())

# Save combined Excel
writer = pd.ExcelWriter("/Users/margheritabisaglia/Library/CloudStorage/OneDrive-ScientificNetworkSouthTyrol/PhD/Courses/Python 2025/HR_hot_all.xlsx") 
for name, df in HR_hot_dict.items():
    df.to_excel(writer, sheet_name=name)
writer.close()  


