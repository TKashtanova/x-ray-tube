"""
Cut phase-space file to fit a square aperture + margin 
by Tatiana Kashtanova
09/2023
"""

# Libraries
import os
import pandas as pd
#import numpy as np



# INPUTS
# Aperture side size (mm)
side = 15
# Margin around the aperture (mm)
m = 0.5
# Sensitive detector half-size (mm)
sd = 25
# Path to phase-space file
path_sim = 'D:/output/56 mm/143 kVp/Livermore directional/cu0.0225 with al0.7+cu0.025'
# Path to save output
path_save = 'D:/output/56 mm/143 kVp/col cu0.0225 with al0.7+cu0.025/col5'


# Aperture half-size in mm
apt = side/2

# Read data
os.chdir(path_sim)
df = pd.read_csv("photons.csv")
row = []
for i in range(len(df)): 
    xx = df.at[i,"pos_x,mm"]
    zz = df.at[i,"pos_z,mm"]
    if zz >= -10-apt-m and zz <= -10+apt+m:
        if xx >= -apt-m and xx <= apt+m:
            row.append(i)   
data = df.iloc[row] 
data_name = os.path.join(path_save, 'col_' + str(side) + '_' + str(side) + '.csv')
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
#txt = "Total Counts: " + str(len(data))
#plt.text(-12.5, 0, txt , horizontalalignment = "left", fontsize = 16, backgroundcolor = "white")
plt.show()
'''







