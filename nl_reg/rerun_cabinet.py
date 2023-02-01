"""
This script re-runs cabinet
Arguments:
    sub: subject ID including "sub-"
    ses: ses ID including "ses-"
    ants_wd: ANTS working dir
    derivs: CABINET derivatives folder
    code_dir: located of cabinet_run_new.sh
    bids_input: raw input data location
Usage:
  run_bibsnet <sub> <ses> <ants_wd> <derivs> <code_dir> <bids_input>
  run_bibsnet -h | --help
Options:
  -h --help     Show this screen.
"""

import os
import subprocess
import glob
from docopt import docopt

def run_bibsnet(sub,ses,ants_wd,derivs,code_dir,bids_input):
    new_inputs=os.path.join(ants_wd,sub)
    bibsnet_derivs='{}/bibsnet'.format(derivs)
    subses='{}_{}'.format(sub,ses)

    bibsnet_out=os.path.join(bibsnet_derivs, sub, ses, 'output')
    os.system('rm {}/*'.format(bibsnet_out))

    bibsnet_in=os.path.join(bibsnet_derivs, sub, ses, 'input')
    for Tx in ['0','1']:
        os.system('cp {}/preBIBSnet_final_000{}.nii.gz {}/{}_{}_optimal_resized_000{}.nii.gz'.format(new_inputs,Tx,bibsnet_in,sub,ses,Tx))

    os.chdir(new_inputs)
    os.system('{}/cabinet_run_new.sh {} {} {}'.format(code_dir,bids_input,derivs,sub.strip('sub-')))

if __name__ == '__main__':
    args = docopt(__doc__)
    run_bibsnet(args['<sub>'], args['<ses>'], args['<ants_wd>'], args['<derivs>'],  args['<code_dir>'], args['<bids_input>'])
