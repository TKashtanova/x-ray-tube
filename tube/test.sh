#!/bin/bash -l
#SBATCH --job-name="model"
#SBATCH --output="Log_model"
#SBATCH --partition=parallel
#SBATCH -t 00-01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=48
#SBATCH --export=ALL

 
source /scratch4/mrezaee1/Geant4-v11.1.1/geant4-v11.1.1-install/bin/geant4.sh 

cd /data/mrezaee1/model/build
ml cmake
cmake ..
make
./tube run.mac

source /scratch4/mrezaee1/root-v6.28.04/root/bin/thisroot.sh 
hadd test.root output0_t{0..47}.root 

