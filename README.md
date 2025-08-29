# Python Final Assignment 2025  

## Project Description and Objectives  

This project analyzes heart rate (HR, bpm) data collected during two experimental campaigns exploring human sensitivity to environmental temperatures

Each experiment was divided into 5 blocks.  

### Experimental Conditions  
- Mild uncomfortable temperatures  
  - Cool: 18 °C ± 1 °C  
  - Warm: 28 °C ± 1 °C 

- Extreme temperatures
  - Cold: 8 °C ± 2 °C  
  - Hot: 38 °C ± 2 °C 

While skin and core temperature had already been analyzed in previous work, the effect of environmental conditions on heart rate had not yet been examined.  

### Project Goals  
1. **Organize the data**  
   - Create `.xlsx` files for each condition (cold, cool, warm, hot).  
   - Each file contains one sheet per participant with three columns:  
     - `time` → time values  
     - `HR` → heart rate values (bpm)  
     - `block` → block number (1–5).  

2. **Compute descriptive statistics**  
   - Mean and standard deviation of HR for each block (1–5).  
   - Mean and standard deviation of HR across all blocks.  

3. **Perform statistical testing**  
   - One-way ANOVA to test for statistical differences between conditions.  

4. **Visualize results**  
   - Histograms showing mean HR values for each condition (per block and overall).  

---

## Repository Structure  
- data_organization.py # Script for creating condition-wise Excel files
- data_analysis.py # Script for statistical analysis and plotting
- README.md # Project documentation
