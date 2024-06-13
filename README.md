# x-ray-tube
FLASH-SARRP X-ray Tube Modeling and Simulation

## Folder: RAD-44 Tube

### cu0.0225 with al0.7+cu0.025
Description: RAD-44 x-ray tube model with (0.0225 mm Cu + 0.7 mm Al) inherent filtration and 0.025 mm Cu external filtration (Geant4)

Inputs (run.mac): electron energy, electron source shape and position, directional bremsstrahlung splitting factor and target, #simulation histories

Outputs: phase-space file in .root (particle position on the scoring plane, energy, momentum direction, and mass)


### cu0.0225 with al0.7+none
Description: RAD-44 x-ray tube model with (0.0225 mm Cu + 0.7 mm Al) inherent filtration and no external filtration (Geant4)

Inputs (run.mac): electron energy, electron source shape and position, directional bremsstrahlung splitting factor and target, #simulation histories

Outputs: phase-space file in .root (particle position on the scoring plane, energy, momentum direction, and mass)


### test.sh
Example of a job submission file for Rockfish

### root.py
Description: post-processing of Geant4 .root file (Python)

Inputs: tube peak kilovoltage, sensitive detector half-size, path to .root file

Outputs: phase-space file in .csv (particle position on the scoring plane, energy, momentum direction, and mass), plot of particle position on the scoring plane, spectrum plot, notes on the simulation (#particles, minimum, maximum, and average energy)


## Folder: Phantom Irradiation

### col5
Description: phantom irradiation model with 5 mm circular collimator (Geant4)

Inputs: run.mac file

Outputs: deposited dose values in .txt registered by the scoring mesh


### run1.mac
Example of run.mac file initializing a portion of photons

### source_cut_c.py
Description: cuts the phase-space file to fit a circular aperture + margin (Python)

Inputs: collimator diameter, margin around the aperture, sensitive detector half-size, path to phase-space file, path to save output

Outputs: reduced phase-space file in .csv (particle position on the scoring plane, energy, momentum direction, and mass), plot of the reduced source on the scoring plane


### source_cut_s.py
Description: cuts the phase-space file to fit a square aperture + margin (Python)

Inputs: aperture side size, margin around the aperture, sensitive detector half-size, path to phase-space file, path to save output

Outputs: reduced phase-space file in .csv (particle position on the scoring plane, energy, momentum direction, and mass), plot of the reduced source on the scoring plane


### source_many.py
Description: generates multiple run.mac files with information on each photon (Python)

Inputs (run.mac): path to photons.csv, mf.txt, and mf_cut.txt files

Outputs: multiple run.mac files

### mf.txt
Example of mf.txt file (contains a number representing photon multiplication factor)

### mf_cut.txt
Example of mf_cut.txt file (contains a number representing the portion of photons initialized in a single run.mac file)

### mesh_data.m
Description: Merging and post-processing of dose deposition .txt files obtained in Geant4 (MATLAB)

Inputs (run.mac): #simulation histories, files numbering, path to the data

Outputs: dose-rate in 1 and 2 tubes, longitudinal and crossbeam dose-rate profiles


## Folder: HVL

### NIST Tables
NIST data for Al, Cu, and water (energy edges excluded)

### hvl_math.py
Description: analytical HVL calculation algorithm (Python)

Inputs: tube peak kilovoltage, attenuator material, path to photon energy spectrum, path to NIST Tables, path to save output

Outputs: HVL curve data in .csv, HVL curve plot, HVL1, QVL, HVL2 values

### ph_spect.csv
Example of photon energy spectrum file

