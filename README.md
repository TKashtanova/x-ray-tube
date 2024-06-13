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
