"""
This script converts fsl .mat files to ants warp files and applies warps to average anats to get bibsnet input files
Arguments:
    sub: subject ID including "sub-"
    ses: ses ID including "ses-"
    ants_wd: ANTS working dir
    derivs: CABINET derivatives folder
    mni: mni template dir
Usage:
  apply_warps <sub> <ses> <ants_wd> <derivs> <mni>
  apply_warps -h | --help
Options:
  -h --help     Show this screen.
"""

import os
import params
from docopt import docopt

def apply_warps(sub,ses,ants_wd,derivs,mni,code_dir):
    #os.system('module load ants')

    subses='{}_{}'.format(sub,ses)
    sub_wd = os.path.join(ants_wd, sub, ses)
    nnunet_inputs=os.path.join(sub_wd, 'nnunet')

    # create nnunet folder
    if not os.path.exists(nnunet_inputs):
        os.makedirs(nnunet_inputs)
    
    #Convert mat files and apply warps if not done already:
    if not os.path.exists('{}/preBIBSnet_final_0001.nii.gz'.format(nnunet_inputs)):
        # convert T1w_full2crop.mat and T2w_full2crop.mat to ANTS warps
        for Tx in ['T1','T2']:
            if Tx == 'T1':
                tnum='0'
            else:
                tnum='1'

            ref='{}/prebibsnet/{}/{}/cropped/{}w/{}_000{}.nii.gz'.format(derivs,sub,ses,Tx,subses,tnum)
            src='{}/prebibsnet/{}/{}/averaged/{}_000{}.nii.gz'.format(derivs,sub,ses,subses,tnum)
            out='{}/{}w_full2crop_ants.txt'.format(sub_wd,Tx)
            full2cropmat='{}/prebibsnet/{}/{}/resized/ACPC_align/{}w_full2crop.mat'.format(derivs,sub,ses,Tx)

            os.system('c3d_affine_tool -ref {} -src {} {} -fsl2ras -oitk {}'.format(ref,src,full2cropmat,out))
            #print('\n' + 'c3d_affine_tool -ref {} -src {} {} -fsl2ras -oitk {}'.format(ref,src,full2cropmat,out))

        # Convert cropT2tocropT1.mat to ANTS warp
        ref='{}/prebibsnet/{}/{}/cropped/T1w/{}_0000.nii.gz'.format(derivs,sub,ses,subses)
        src='{}/prebibsnet/{}/{}/cropped/T2w/{}_0001.nii.gz'.format(derivs,sub,ses,subses)
        matfile='{}/prebibsnet/{}/{}/resized/xfms/cropT2tocropT1.mat'.format(derivs,sub,ses)
        os.system('c3d_affine_tool -ref {} -src {} {} -fsl2ras -oitk {}/cropT2tocropT1_ants.txt'.format(ref,src,matfile,sub_wd))
        #print('\n' + 'c3d_affine_tool -ref {} -src {} {} -fsl2ras -oitk {}/cropT2tocropT1_ants.txt'.format(ref,src,matfile,sub_wd))

        # Apply warps
        mni='{}/INFANT_MNI_T2_1mm.nii.gz'.format(mni)
        t2_antswarp='{}/antsregWarp.nii.gz'.format(sub_wd)
        t2_antsaffine='{}/antsregAffine.txt'.format(sub_wd)

        # T1
        src='{}/prebibsnet/{}/{}/averaged/{}_0000.nii.gz'.format(derivs,sub,ses,subses)
        out='{}/preBIBSnet_final_0000.nii.gz'.format(nnunet_inputs)
        t1full2crop='{}/T1w_full2crop_ants.txt'.format(sub_wd)
        os.system('WarpImageMultiTransform 3 {} {} -R {} {} {} {}'.format(src,out,mni,t1full2crop,t2_antswarp,t2_antsaffine))
        #print('\n' + 'WarpImageMultiTransform 3 {} {} -R {} {} {} {}'.format(src,out,mni,t1full2crop,t2_antswarp,t2_antsaffine))

        # T2
        src='{}/prebibsnet/{}/{}/averaged/{}_0001.nii.gz'.format(derivs,sub,ses,subses)
        out='{}/preBIBSnet_final_0001.nii.gz'.format(nnunet_inputs)
        t2full2crop='{}/T2w_full2crop_ants.txt'.format(sub_wd)
        crop2crop='{}/cropT2tocropT1_ants.txt'.format(sub_wd)
        os.system('WarpImageMultiTransform 3 {} {} -R {} {} {} {} {}'.format(src,out,mni,t2full2crop,crop2crop,t2_antswarp,t2_antsaffine))
        #print('\n' + 'WarpImageMultiTransform 3 {} {} -R {} {} {} {} {}'.format(src,out,mni,t2full2crop,crop2crop,t2_antswarp,t2_antsaffine))

    #Run nnunet
    os.system('{}/infer.sh {} {}'.format(code_dir, sub_wd, nnunet_inputs))

if __name__ == '__main__':
    args = docopt(__doc__)
    apply_warps(args['<sub>'], args['<ses>'], args['<ants_wd>'], args['<derivs>'],  args['<mni>'])