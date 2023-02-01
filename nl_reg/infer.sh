#!/bin/bash
sbatch <<EOT
#!/bin/bash -l

#SBATCH --job-name=nnunet
#SBATCH --mem=64g 
#SBATCH --time=20:00:00

#SBATCH -p v100
#SBATCH --gres=gpu:v100:2
#SBATCH --ntasks=1
#SBATCH --tmp=40g
#SBATCH --cpus-per-task=24

#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=lmoore@umn.edu
#SBATCH -e $1/nnunet-%j.err
#SBATCH -o $1/nnunet-%j.out

#SBATCH -A feczk001

## build script here
module load gcc cuda/11.2
source /panfs/roc/msisoft/anaconda/anaconda3-2018.12/etc/profile.d/conda.sh
conda activate /home/support/public/torch_cudnn8.2

export nnUNet_raw_data_base="/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base"
export nnUNet_preprocessed="/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_preprocessed"
export RESULTS_FOLDER="/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_trained_models"

nnUNet_predict -i $2 -o $1 -t 550 -m 3d_fullres
EOT