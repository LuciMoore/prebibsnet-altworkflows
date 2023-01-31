import numpy as np
import nibabel as nib
import os
import glob
from nipype.interfaces import fsl
import shutil


def register_and_average_files(input_file_paths, output_file_path):
    reference = input_file_paths[0]
    if len(input_file_paths) > 1:
        registered_files = register_files(input_file_paths, reference)

        create_avg_image(output_file_path, registered_files)
    else:
        shutil.copyfile(reference, output_file_path)


def create_avg_image(output_file_path, registered_files):
    """
    :param output_file_path: String, valid path to average image file to make
    :param registered_files: List of strings; each is a valid path to an
                             existing image file to add to the average
    """
    np.set_printoptions(precision=2, suppress=True)  # Set numpy to print only 2 decimal digits for neatness
    first_nifti_file = registered_files[0]
    n1_img = nib.load(first_nifti_file)
    header = n1_img.header
    data_dtype = header.get_data_dtype()
    sum_matrix = n1_img.get_fdata().copy()
    n = len(registered_files)
    for j in range(1, n):
        img = nib.load(registered_files[j])
        data = img.get_fdata().copy()
        sum_matrix += data
    avg_matrix = sum_matrix / n
    if data_dtype == np.int16:
        avg_matrix = avg_matrix.astype(int)
    new_header = n1_img.header.copy()
    new_img = nib.nifti1.Nifti1Image(avg_matrix, n1_img.affine.copy(), header=new_header)
    nib.save(new_img, output_file_path)

def register_files(input_file_paths, reference):
    registered_files = [reference]
    flt = fsl.FLIRT(bins=640, cost_func='mutualinfo')
    flt.inputs.reference = reference
    flt.inputs.output_type = "NIFTI_GZ"
    for structural in input_file_paths[1:]:
        flt.inputs.in_file = structural
        print(flt.cmdline)
        out_index = flt.cmdline.find('-out')
        start_index = out_index + len('-out') + 1
        end_index = flt.cmdline.find(' ', start_index)
        out = flt.cmdline[start_index:end_index]
        registered_files.append(out)
        res = flt.run()
        stderr = res.runtime.stderr
        if stderr:
            err_msg = 'flirt error message: {stderr}'
            raise RuntimeError(err_msg)
    return registered_files

wd = '/home/feczk001/shared/projects/nnunet_predict/task550_testing/hypernorm/templates/0mo'

os.chdir(os.path.join(wd, 'T2s'))
anats = glob.glob('*0001.nii.gz')
out = os.path.join(wd, '0mo_T2_average.nii.gz')
register_and_average_files(anats, out)


'''
os.chdir(os.path.join(wd, 'T1s'))
anats = glob.glob('*0000.nii.gz')
out = os.path.join(wd, '0mo_T1_average.nii.gz')
register_and_average_files(anats, out)

'''

