import argparse
import glob
import os
import numpy as np
import torch
import nibabel as nib
from nibabel import processing

from functools import partial
from tqdm import tqdm as std_tqdm
tqdm = partial(std_tqdm, dynamic_ncols=True)

from utils.load_model import load_model
from utils.preprocessing import N4_Bias_Field_Correction
from utils.cropping import cropping
from utils.stripping import stripping
from utils.parcellation import parcellation
from utils.hemisphere import hemisphere
from utils.postprocessing import postprocessing

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="input folder")
    parser.add_argument("-o", help="output folder")
    return parser.parse_args()

def main():
    print(
        "\n#######################################################################\n"
        "Please cite the following paper when using OpenMAP-T1:\n"
        "Kei Nishimaki, Kengo Onda, Kumpei Ikuta, Yuto Uchida, Hitoshi Iyatomi, Kenichi Oishi (2024).\n"
        "OpenMAP-T1: A Rapid Deep Learning Approach to Parcellate 280 Anatomical Regions to Cover the Whole Brain.\n"
        "paper: https://www.medrxiv.org/content/10.1101/2024.01.18.24301494v1.\n"
        "#######################################################################\n"
        )
    opt = create_parser()
    device = torch.device("cuda") if torch.cuda.is_available() else "cpu"
    cnet, ssnet, pnet_c, pnet_s, pnet_a, hnet_c, hnet_a = load_model(device)
    pathes = sorted(glob.glob(os.path.join(opt.i, "**/*.nii"), recursive=True))
    print(f"We found {len(pathes)} images")
    
    DATASET = opt.o
    OUTPUT_SS_PATH = DATASET + "/unified"
    OUTPUT_PARCELLATION_PATH = DATASET + "/parcellation"
    os.makedirs("N4", exist_ok=True)
    os.makedirs(OUTPUT_SS_PATH, exist_ok=True)
    os.makedirs(OUTPUT_PARCELLATION_PATH, exist_ok=True)
    
    for ipath in tqdm(pathes):
        ### 重要!! 保存名自分で設定する必要がある ###
        opath = os.path.basename(ipath)
        ##########################################
        
        N4_Bias_Field_Correction(ipath, f"N4/N4.nii")
        odata = nib.squeeze_image(nib.as_closest_canonical(nib.load(f"N4/N4.nii")))
        data = processing.conform(
            odata, out_shape=(256, 256, 256), voxel_size=(1.0, 1.0, 1.0), order=1
        )
        cropped = cropping(data, cnet, device)
        stripped, stripped_shift, shift = stripping(cropped, data, ssnet, device)
        nii = nib.Nifti1Image(stripped.astype(np.float32), affine=data.affine)
        nib.save(nii, f"{OUTPUT_SS_PATH}/{opath}")
        
        parcellated = parcellation(stripped_shift, pnet_c, pnet_s, pnet_a, device)
        separated = hemisphere(stripped_shift, hnet_c, hnet_a, device)
        output = postprocessing(parcellated, separated, shift, device)
        nii = nib.Nifti1Image(output.astype(np.uint16), affine=data.affine)
        nib.save(nii, f"{OUTPUT_PARCELLATION_PATH}/{opath}")
        gaga
        # nibabel, tqdm, simpleitk, scipy, ants
    
if __name__ == "__main__":
    main()