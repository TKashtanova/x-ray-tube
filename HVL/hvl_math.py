"""
HVL analytical calculation algorithm 
by Tatiana Kashtanova
03/2024
"""
   
# Libraries
import os
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt


# INPUTS
# Tube peak kilovoltage [kVp]
kVp = 143
# Attenuator material ("al" or "cu")
material = "al"
# Path to photon energy spectrum
path_sp = 'D:/output/56 mm/143 kVp/Livermore directional/cu0.0225 with al0.7+none'
# Path to NIST tables
path_nist = 'D:/output/NIST Tables'
# Path to save output
path_save = 'D:/output/'



# Photon energy spectrum
os.chdir(path_sp) 
df = pd.read_csv("ph_spectr.csv")
# Exclude photons with mean energy < 10% tube kVp
r_st = int(0.1*kVp)
df = df.iloc[r_st:,:]
df.reset_index(inplace = True, drop = True)


# NIST tables (energy edges excluded)
os.chdir(path_nist) 
nist_cu = pd.read_csv("Copper.csv")
nist_al = pd.read_csv("Aluminum.csv")
nist_water = pd.read_csv("Water.csv")
# Convert NIST energy in MeV to keV
def nist(data):
    data["Energy,MeV"] = data["Energy,MeV"].apply(lambda x: x*1000)
    data.columns.values[0] = "Energy,keV"
    return data
nist_cu = nist(nist_cu)
nist_al = nist(nist_al)
nist_water = nist(nist_water)


# Attenuator specific parameters
if material == "cu":
    # Copper NIST table
    nist_f = nist_cu
    # Copper density [g/cm3]
    ro = 8.96
    # Copper thickness [mm]
    dcu_mm = np.arange(0, 1, 0.01).tolist()
    dcu_mm = [round(elem, 2) for elem in dcu_mm]
    d_mm = dcu_mm    
else:
    # Aluminum NIST table
    nist_f = nist_al
    # Aluminum density [g/cm3]
    ro = 2.7
    # Aluminum thickness [mm]
    dal_mm = np.arange(0, 3.6, 0.5).tolist()
    l1 = np.arange(3.6, 4.15, 0.05).tolist()
    dal_mm.extend(l1)
    l2 = np.arange(4.15, 10.2, 0.5).tolist()
    dal_mm.extend(l2)
    l3 = np.arange(10.2, 11.6, 0.05).tolist()
    dal_mm.extend(l3)
    l4 = np.arange(11.6, 19.6, 0.5).tolist()
    dal_mm.extend(l4)
    dal_mm = [round(elem, 2) for elem in dal_mm]
    d_mm = dal_mm   
# Attenuator thickness [cm]
d_cm = [round((x/10),3) for x in d_mm]

# Sensitive detector surface area [cm2]
a = 0.145

# NIST table interpolation function  
def interpolate_nist(nist_table, en_value, coef_column):
    # List available NIST energy values
    nist_en_list = list(nist_table.iloc[:,0])
    # y - energy, x - coefficeint
    # y = ax + b
    if en_value in nist_en_list:
        row = nist_en_list.index(en_value)
        x = nist_table.iloc[row,coef_column]
        x_coef = x
    else:
        # The closest energy values in NIST table
        y1 = max([j for j in nist_en_list if en_value > j])
        row1 = nist_en_list.index(y1)
        y2 = nist_table.iloc[row1+1,0]
        # The corresponding coefficients in NIST table
        x1 = nist_table.iloc[row1,coef_column]
        x2 = nist_table.iloc[row1+1,coef_column]
        if x1 == x2:
            x = x1
        else:
            # Log-log interpolation
            y1_log = math.log(y1,10)
            y2_log = math.log(y2,10)
            x1_log = math.log(x1,10)
            x2_log = math.log(x2,10)
            # Slope: a = (y1-y2)/(x1-x2)
            a = (y1_log - y2_log)/(x1_log - x2_log)
            # Y-intercept: b = y - ax
            b = y1_log - a*x1_log
            # Coefficient: x = (y-b)/a
            x = (math.log(en_value,10)-b)/a
            x_coef = 10**(x)
    return x_coef

    
# Dose calculation function   
def compute_dose(df, d, ro, nist_f):
    df_calc = pd.DataFrame(columns = ["E_mean,keV", "N0", "mu/ro", "mu", "l", "N", "mu/ro2", "Dose, Gy"])
    for i in range(len(df)):
        en_i = df.at[i,"mean"]
        n0_i = df.at[i,"counts"]
        # E_keV - mean energy of the corresponding energy bin [keV] 
        df_calc.at[i,"E_mean,keV"] = en_i
        # N0 - initial #photons
        df_calc.at[i, "N0"] = n0_i
        # mu/ro - mass attenuation coefficient [cm2/g]
        df_calc.at[i, "mu/ro"] = interpolate_nist(nist_f, en_i, 1)
        # mu - linear attenuation coefficient [1/cm]        
        df_calc.at[i, "mu"] = df_calc.at[i, "mu/ro"]*ro
        # Depth [cm]
        df_calc.at[i, "l"] = d
        # N - #photons passed though the attenuator
        df_calc.at[i, "N"] = int(n0_i*math.exp(-df_calc.at[i, "mu"]*d))
        # mu/ro2 - mass energy-absorption coefficient [cm2/g]
        df_calc.at[i, "mu/ro2"] = interpolate_nist(nist_water, en_i, 2)
        # Unit conversion coefficient 
        coef = 1.60218e-13
        # Dose [Gy]
        df_calc.at[i, "Dose, Gy"] = (df_calc.at[i, "N"]/a)*en_i*df_calc.at[i, "mu/ro2"]*coef
    return df_calc
 
    
# HVL curve calculation function 
def hvl_curve(df):
    out = pd.DataFrame(columns = ["filter, mm", "D", "D_norm"])
    for i in range(len(d_cm)):
        out.at[i, "filter, mm"] = d_mm[i]
        D_calc = compute_dose(df, d_cm[i], ro, nist_f)
        out.at[i, "D"] = sum(D_calc["Dose, Gy"])
        out.at[i, "D_norm"] = out.at[i, "D"]/out.at[0, "D"]
    return out

# HVL curve interpolation function  
def interpolate_curve(df, v):
    # List of normalized dose values
    v_list = list(df.loc[:, "D_norm"])
    # y - normalized dose value, x - thickness [mm]
    # y = ax + b
    if v in v_list:
        row = v_list.index(v)
        x = df.loc[row, "filter, mm"]
    else:
        # The closest min dose value 
        y1 = max([j for j in v_list if v > j])
        row1 = v_list.index(y1)
        y2 = df.loc[row1-1, "D_norm"]
        x1 = df.loc[row1,"filter, mm"]
        x2 = df.loc[row1-1,"filter, mm"]
        # Slope: a = (y1-y2)/(x1-x2)
        a = (y1 - y2)/(x1 - x2)
        # Y-intercept: b = y - ax
        b = y1 - a*x1
        # Thickness: x = (y-b)/a
        x = (v-b)/a
    return x


# Compute HVL curve 
df_out = hvl_curve(df)
# Save HVL curve data as .csv
os.chdir(path_save) 
name = "df_" + material + ".csv"
df_out.to_csv(name, index = False)

# Plot HVL curve
unit = material + ', mm'
fig, ax = plt.subplots(figsize = (8, 8))
plt.plot(df_out["filter, mm"], df_out["D_norm"], linestyle="-", marker="o", ms = 3, c = "tab:blue")
plt.axhline(y = 0.5, color = "black", linestyle = "dashed", linewidth = 1.2, dashes = (5, 5)) 
plt.axhline(y = 0.25, color = "black", linestyle = "dashed", linewidth = 1.2, dashes = (5, 5)) 
plt.xlabel(unit, fontsize = 16, labelpad = 15)
plt.ylabel("Normalized values", fontsize = 16)
plt.xticks(fontsize = 16, rotation = 0)
plt.yticks(fontsize = 16, rotation = 0)
plt.grid()
plt.show()

# Display HVL1, QVL, and HVL2 
# Round the result to 2 or 3 decimal points
if material == "cu":
    r = 3
else:
    r = 2
print("\n")
hvl1 = round(interpolate_curve(df_out, 0.5),r)
print("HVL1:", hvl1, " mm")
qvl = round(interpolate_curve(df_out, 0.25),r)
print("QVL:", qvl, " mm")
hvl2 = round((qvl - hvl1),r)
print("HVL2:", hvl2, " mm")

