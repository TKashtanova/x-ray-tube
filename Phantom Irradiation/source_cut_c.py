"""
Cut phase-space file to fit a circular aperture + margin 
by Tatiana Kashtanova
09/2023
"""

# Libraries
import os
import pandas as pd
import numpy as np



# INPUTS
# Collimator diameter (mm)
col_d = 5
# Margin around the aperture (mm)
m = 0.5
# Sensitive detector half-size (mm)
sd = 25
# Path to phase-space file
path_sim = 'D:/output/56 mm/143 kVp/Livermore directional/cu0.0225 with al0.7+cu0.025'
# Path to save output
path_save = 'D:/output/56 mm/143 kVp/col cu0.0225 with al0.7+cu0.025/col5'


# Aperture radius in mm 
r_a = col_d/2

# Read data
os.chdir(path_sim) 
df = pd.read_csv("photons.csv")
row = []
for i in range(len(df)): 
    xx = df.at[i,"pos_x,mm"]
    z = df.at[i,"pos_z,mm"]
    zz = z+10
    r = np.sqrt(np.square(xx) + np.square(zz)) 
    if r <= r_a + m:
        row.append(i)   
data = df.iloc[row] 
data_name = os.path.join(path_save, "col_" + str(int(r_a*2)) + ".csv")
data.to_csv(data_name, index = False)
print(len(data))

'''
# Visualization of the reduced source
import matplotlib.pyplot as plt
plt.figure(figsize = (6, 6))
plt.scatter(data["pos_z,mm"], data["pos_x,mm"], c = data["energy,keV"], cmap = "magma")
plt.xlabel("z,mm", fontsize = 15)
plt.ylabel("x,mm", fontsize = 15)
plt.grid()
if r_a == 5:
    plt.xticks(np.arange(-16, -3), fontsize = 12)
    plt.yticks(np.arange(-6, 7), fontsize = 12)
txt_title = "Aperture diameter: " + str(r_a*2) + " mm"
plt.title(txt_title, fontsize = 14)
#txt = "Total Counts: " + str(len(data))
#plt.text(-12.5, 0, txt , horizontalalignment = "left", fontsize = 16, backgroundcolor = "white")
plt.show()
'''





