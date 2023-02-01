"""
This script runs nonlinear registration on subject anatomicals to MNI templates
Arguments:
    wd: ANTS working dir
    derivs: CABINET derivatives folder
    sub: subject ID including "sub-"
    ses: ses ID including "ses-"
    mni: templates folder
    code_dir: path to code folder
Usage:
  nonlinear_reg <wd> <derivs> <sub> <ses> <mni> <code_dir>
  nonlinear_reg -h | --help
Options:
  -h --help     Show this screen.
"""

import os
from docopt import docopt
import shutil

def nonlinear_reg(wd,derivs,sub,ses,mni,code_dir):
    #create working directory for subject-session
    sub_wd = os.path.join(wd, sub, ses)

    if os.path.exists(os.path.join(sub_wd, 'T2w_NL_reg.nii.gz')):
        print('Nonlinear registration for this subject already complete')
    else:
        if not os.path.exists(sub_wd):
            os.makedirs(sub_wd)
        
        #Define path of cropped T1-registered T2 from bibsnet derivatives to NL register to MNI atlas
        input_anat='{}/prebibsnet/{}/{}/resized/xfms/T2w_registered_to_T1w.nii.gz'.format(derivs,sub,ses)
        template='{}/INFANT_MNI_T2_1mm.nii.gz'.format(mni)
        out='{}/T2w_NL_reg.nii.gz'.format(sub_wd)

        os.chdir(sub_wd)
        os.system('{}/nl_reg.sh {} {} {}'.format(code_dir, template, input_anat, out))

if __name__ == '__main__':
    args = docopt(__doc__)
    nonlinear_reg(args['<wd>'], args['<derivs>'], args['<sub>'], args['<ses>'], args['<mni>'], args['<code_dir>'])
