#!/bin/bash
sbatch <<EOT
#!/bin/bash -l

#SBATCH -t 2:00:00
#SBATCH --mem-per-cpu=32GB
#SBATCH --cpus-per-task=4
#SBATCH --partition=msismall
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lmoore@umn.edu
#SBATCH -o ants.out
#SBATCH -e ants.err
#SBATCH -J ANTS
#SBATCH -A feczk001

module load ants

# Register the template head to the subject head
ANTS 3 -m \
CC[$1,$2,1,5] \
-t SyN[0.25] -r Gauss[3,0] -o antsreg -i 60x50x20 --use-Histogram-Matching \
--number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000

antsApplyTransforms -d 3 \
  --output $3 \
  --reference-image $1 \
  --transform antsregWarp.nii.gz antsregAffine.txt \
  --input $2 \
  --interpolation BSpline

EOT