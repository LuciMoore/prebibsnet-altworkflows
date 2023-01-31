import os

os.chdir('/home/feczk001/shared/projects/nnunet_predict/task550_testing/hypernorm/')
Tx='T2'

if Tx=='T1':
    orig_anat='orig/sub-838631_ses-V02_optimal_resized_0000.nii.gz'
    template='templates/0mo_T1_average.nii.gz'
    out='norm/0mo/sub-838631_ses-V02_optimal_resized_0000.nii.gz'

else:
    orig_anat='orig/sub-838631_ses-V02_optimal_resized_0001.nii.gz'
    template='templates/0mo_T2_average.nii.gz'
    out='norm/0mo/sub-838631_ses-V02_optimal_resized_0001.nii.gz'

cmd='fslmaths {} -sub `fslstats {} -M` -div `fslstats {} -S` -mul `fslstats {} -S` -add `fslstats {} -M` {}'.format(orig_anat,orig_anat,orig_anat,template,template,out)
os.system(cmd)