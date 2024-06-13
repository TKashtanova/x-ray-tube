"""
Generate multiple run.mac files with information on each photon
by Tatiana Kashtanova
09/2023
"""


# Libraries
import os
import pandas as pd


# INPUTS
# Path to photons.csv, mf.txt, and mf_cut.txt files location
os.chdir('D:/output/56 mm/143 kVp/col cu0.0225 with al0.7+cu0.025/col5')




# Multiplication factor / #photons per 1 run.mac
mf_data = pd.read_csv("mf.txt", sep = " ", header = None)
mf = mf_data.iloc[0,0]
v_cut_data = pd.read_csv("mf_cut.txt", sep = " ", header = None)
v_cut = v_cut_data.iloc[0,0]


# Read data
df = pd.read_csv("col.csv")
# A list of row indices in .csv file
row_id = [i for i in range(len(df))]
# Indices of the output files which contain a portion of the original photons  
file_n = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] 
 

# Function writing the info about the photons from the selected .csv rows   
def source(name, n, s, e):
    if e>len(df.index):
        e == len(df.index)
    run = open(name,"w")
    run.write("/score/create/boxMesh boxMesh_1 \n")
    run.write("/score/mesh/boxSize 25 10 25 mm \n")
    run.write("/score/mesh/nBin 250 20 250 \n")
    run.write("/score/mesh/translate/xyz 0. -71. -10. mm \n")
    run.write("/score/quantity/doseDeposit dDep \n")
    run.write("/score/close \n\n")
    
    data = df.copy(deep = True)
    data = data.iloc[s:e]
    data.reset_index(inplace = True, drop = True)
    print(len(data))
    for i in range(len(data.index)):
        run.write("/gps/source/add 1 \n")
        run.write("/gps/source/intensity 1 \n")
        run.write("/gps/particle gamma \n")
        energy = round(data["energy,keV"][i],2)
        en_command = "/gps/energy " + str(energy) + " keV \n"
        run.write(en_command)
        run.write("/gps/pos/type Point \n")
        pos_x = round(data["pos_x,mm"][i],8)
        pos_y = round(data["pos_y,mm"][i],8)
        pos_z = round(data["pos_z,mm"][i],8)
        pos_command = "/gps/pos/centre " + str(pos_x) + " " + str(pos_y) + " " + str(pos_z) + " mm \n"
        run.write(pos_command)
        dir_x = round(data["dir_x,mm"][i],8)
        dir_y = round(data["dir_y,mm"][i],8)
        dir_z = round(data["dir_z,mm"][i],8)
        dir_command = "/gps/direction " + str(dir_x) + " " + str(dir_y) + " " + str(dir_z) + " \n\n"
        run.write(dir_command)  
    
    run.write("/gps/source/multiplevertex true \n")
    run_beam = "/run/beamOn " + str(mf) + " \n"
    run.write(run_beam)
    dose_name = "/score/dumpQuantityToFile boxMesh_1 dDep " + "dDep_" + str(n+1) + ".txt"
    run.write(dose_name)
    run.close()

j = 0
for r in range(0, len(row_id),v_cut):       
    run_name = "run" + file_n[j] + ".mac"
    source(run_name, j, r, r+v_cut)
    j = j+1