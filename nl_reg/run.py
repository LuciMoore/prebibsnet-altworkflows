import nl_reg
import rerun_cabinet
import fsl2ants
import params
import os

sub=params.sub
ses=params.ses
stage=params.stage
wd=params.ants_wd
derivs=params.derivs
mni=params.mni
code_dir=params.code_dir
bids_input=params.bids_input

if stage == 'stage1':
    nl_reg.nonlinear_reg(wd,derivs,sub,ses,mni,code_dir)

elif stage == 'stage2':
    fsl2ants.apply_warps(sub,ses,wd,derivs,mni, code_dir)
