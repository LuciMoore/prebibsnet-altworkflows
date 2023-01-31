#!/bin/bash
#SBATCH --job-name=task550
#SBATCH --mem=64g        # memory per cpu-core (what is the default?)
#SBATCH --time=20:00:00          # total run time limit (HH:MM:SS)

#SBATCH -p v100
#SBATCH --gres=gpu:v100:2
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --tmp=40g
#SBATCH --cpus-per-task=24

#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=lmoore@umn.edu
#SBATCH -e t550-%j.err
#SBATCH -o t550-%j.out

#SBATCH -A feczk001

## build script here
module load gcc cuda/11.2
source /panfs/roc/msisoft/anaconda/anaconda3-2018.12/etc/profile.d/conda.sh
conda activate /home/support/public/torch_cudnn8.2

export nnUNet_raw_data_base="/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base"
export nnUNet_preprocessed="/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_preprocessed"
export RESULTS_FOLDER="/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_trained_models"

nnUNet_predict -i /home/feczk001/shared/projects/nnunet_predict/task550_testing/nnunet/input \
-o /home/feczk001/shared/projects/nnunet_predict/task550_testing/nnunet/output -t 550 -m 3d_fullres
