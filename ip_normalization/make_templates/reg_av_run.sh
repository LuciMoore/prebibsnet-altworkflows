#!/bin/bash

#SBATCH --job-name=average_templates
#SBATCH --mem-per-cpu=32GB
#SBATCH --time=10:00:00
#SBATCH --cpus-per-task=4
#SBATCH --partition=amdsmall

#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=lmoore@umn.edu
#SBATCH -e %A_log_average_templates.err 
#SBATCH -o %A_log_average_templates.out 

#SBATCH -A feczk001

source /home/faird/shared/code/external/envs/miniconda3/load_miniconda3.sh
conda activate cabinet
module load fsl

python reg_and_average.py