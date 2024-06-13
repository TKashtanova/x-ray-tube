"""
Post-processing of Geant4 .root file
by Tatiana Kashtanova
04/2023
"""

# Import libraries
import os
import uproot as up
import awkward as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable



# INPUTS
# Tube peak kilovoltage [kVp]
kVp = 143
# Sensitive detector half-size [mm]
sd = 25
# Path to .root file
path_sim = 'D:/output/56 mm/143 kVp/Livermore directional/cu0.0225 with al0.7+cu0.025'



# Read data
os.chdir(path_sim) 
f = up.open("test.root")
t = f["Hits"]
t.show()

# Record .root variables as numpy arrays
event = ak.to_numpy(f["Hits/fEvent"].array())
pos_x = ak.to_numpy(f["Hits/fXPosition"].array())
pos_y = ak.to_numpy(f["Hits/fYPosition"].array())
pos_z = ak.to_numpy(f["Hits/fZPosition"].array())
dir_x = ak.to_numpy(f["Hits/fXDirection"].array())
dir_y = ak.to_numpy(f["Hits/fYDirection"].array())
dir_z = ak.to_numpy(f["Hits/fZDirection"].array())
energy = ak.to_numpy(f["Hits/fEnergy"].array())
mass = ak.to_numpy(f["Hits/fMass"].array())

# Record data as a pandas dataframe
df = pd.DataFrame()
df["event"] = event
df["pos_x,mm"] = pos_x
df["pos_y,mm"] = pos_y
df["pos_z,mm"] = pos_z
df["dir_x,mm"] = dir_x
df["dir_y,mm"] = dir_y
df["dir_z,mm"] = dir_z
df["energy,keV"] = energy*1000
df["mass,MeV"] = mass
df["mass,MeV"].unique()

# Save photon and electron dataframes as .csv
ph = df[df["mass,MeV"] == 0]
el = df[round(df["mass,MeV"],2) == 0.51]
ph.to_csv("photons.csv", index = False)
el.to_csv("electrons.csv", index = False)


# Position of particles on the sensitive detector
def plot_pos(data, plt_title):   
    plt.figure(figsize=(13, 10)) 
    plt.scatter(data["pos_z,mm"], data["pos_x,mm"], c=data["energy,keV"], cmap = "magma")
    plt.xlabel("z,mm", fontsize = 16)
    plt.ylabel("x,mm", fontsize = 16)
    clb = plt.colorbar()
    clb.set_label("Energy,keV", size = 18)
    clb.ax.tick_params(labelsize = 12) 
    plt.title(plt_title, fontsize = 18)
    plt.grid()
    plt.xticks(np.arange(-sd-10, sd-9, step=5), fontsize = 12, rotation = 90)
    plt.yticks(np.arange(-sd, sd+1, step=5), fontsize = 12)
    plt.show()
# Photons
#plot_pos(ph, "Photon Position on Scoring Plane")    
# Electrons
#plot_pos(el, "Electron Position on Scoring Plane") 


# Particle energy spectrum using 1 keV bin size
ph_spectr = pd.DataFrame(columns = ["min", "max", "mean", "counts"])
el_spectr = pd.DataFrame(columns = ["min", "max", "mean", "counts"])
i=0
r=0
while i<kVp:
    ph_spectr.loc[r,"min"] = i
    ph_spectr.loc[r,"max"] = i+1
    ph_spectr.loc[r,"mean"] = i+0.5
    ph_spectr.loc[r,"counts"] = len(ph[(ph["energy,keV"] >= i) & (ph["energy,keV"] < (i+1))].index)
    el_spectr.loc[r,"min"] = i
    el_spectr.loc[r,"max"] = i+1
    el_spectr.loc[r,"mean"] = i+0.5
    el_spectr.loc[r,"counts"] = len(el[(el["energy,keV"] >= i) & (el["energy,keV"] < (i+1))].index)
    i = i+1
    r = r+1 
ph_spectr.to_csv("ph_spectr.csv", index = False)
# Exclude photons with energy 7-9 keV
ph_spectr_no7_9 = ph_spectr.copy()
ph_spectr_no7_9.loc[7,"counts"] = 0
ph_spectr_no7_9.loc[8,"counts"] = 0
# The number of excluded photons
excl = ph_spectr.loc[7,"counts"] + ph_spectr.loc[8,"counts"]

# Plot spectrum  
def plot_spectrum(data, plt_ylabel, plt_title, save_name, txt):   
    fig = plt.figure(figsize = (12, 8))
    plt.plot(data["mean"], data["counts"], linestyle="-", marker="o")
    plt.xlabel("Energy,keV", fontsize = 16, labelpad = 15)
    plt.ylabel(plt_ylabel, fontsize = 16)
    plt.title(plt_title, fontsize = 18)
    plt.xticks(np.arange(0, kVp+10, step = 10), fontsize = 14, rotation = 90)
    plt.yticks(fontsize = 14)
    plt.grid()
    if txt != "no":
        fig.text(0.15,-0.02, ("*Note: Photons with [7,9) keV energy (" + str(f"{excl:,}") + " counts) are not shown on this figure"), fontsize = 15, style = "italic")
    #name = os.path.join(path, save_name)
    #plt.savefig(name)
    plt.show()

# Photons    
plot_spectrum(ph_spectr, "Photon counts", "Photon Energy Spectrum", "ph_spectr.png", "no")   
# Photons, excluding those with energy [7,9) keV    
plot_spectrum(ph_spectr_no7_9, "Photon counts", "Photon Energy Spectrum", "ph_spectr_no7_9.png", "yes")   
# Electrons
plot_spectrum(el_spectr, "Electron counts", "Electron Energy Spectrum", "el_spectr.png", "no") 


# Notes on the simulation
ph_ct = '{:,}'.format(sum(ph_spectr["counts"]))
el_ct = '{:,}'.format(len(el.index))
headers = ["Particle", "Count", "Emin, keV", "Emax, keV", "Eavg, keV"]
table = PrettyTable(field_names = headers)
table.add_row(["Photons", ph_ct, \
               round(min(ph["energy,keV"]),2), \
               round(max(ph["energy,keV"]),2), \
               round(ph.loc[:, "energy,keV"].mean(),2)])
table.add_row(["Electrons", el_ct, \
               round(min(el["energy,keV"]),2), \
               round(max(el["energy,keV"]),2), \
               round(el.loc[:, "energy,keV"].mean(),2)])
print(table)
