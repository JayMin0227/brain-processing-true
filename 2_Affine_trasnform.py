import argparse
import glob
import os
import ants
import numpy as np
import nibabel as nib
from nibabel import processing
from functools import partial
from tqdm import tqdm as std_tqdm
tqdm = partial(std_tqdm, dynamic_ncols=True)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="input folder")
    return parser.parse_args()

def main():
    opt = create_parser()
    DATASET = opt.i
    OUTPUT_RIGID_FULL_PATH = DATASET + "/full/rigid"
    OUTPUT_TRSAA_FULL_PATH = DATASET + "/full/trsaa"
    OUTPUT_RIGID_HALF_PATH = DATASET + "/half/rigid"
    OUTPUT_TRSAA_HALF_PATH = DATASET + "/half/trsaa"
    os.makedirs(OUTPUT_RIGID_FULL_PATH, exist_ok=True)
    os.makedirs(OUTPUT_TRSAA_FULL_PATH, exist_ok=True)
    os.makedirs(OUTPUT_RIGID_HALF_PATH, exist_ok=True)
    os.makedirs(OUTPUT_TRSAA_HALF_PATH, exist_ok=True)
    
    pathes = sorted(glob.glob(os.path.join(opt.i, "unified/*.nii"), recursive=True))
    print(f"We found {len(pathes)} images")
    
    for ipath in tqdm(pathes):
        opath = os.path.basename(ipath)
        
        data = nib.squeeze_image(
            nib.as_closest_canonical(nib.load(ipath))
        )
        data_mask = nib.Nifti1Image(
            (data.get_fdata() > 0).astype(np.uint16), affine=data.affine
        )

        MNI_PATH = "/data2/radiology_datas/clean3/MNI/MNI_FULL.nii"
        mni = nib.squeeze_image(nib.as_closest_canonical(nib.load(MNI_PATH)))

        data_ants = ants.from_nibabel(data)
        mask_ants = ants.from_nibabel(data_mask)
        mni_ants = ants.from_nibabel(mni)

        ### Rigid ###
        tx = ants.registration(mni_ants, data_ants, type_of_transform="Rigid")
        data_tx_rigid = nib.as_closest_canonical(ants.to_nibabel(tx["warpedmovout"]))
        data_mask_tx_rigid = nib.as_closest_canonical(
            ants.to_nibabel(
                ants.apply_transforms(
                    fixed=mni_ants,
                    moving=mask_ants,
                    transformlist=tx["fwdtransforms"],
                    interpolator="nearestNeighbor",
                )
            )
        )
        data_tx_rigid = nib.Nifti1Image(
            (data_tx_rigid.get_fdata() * data_mask_tx_rigid.get_fdata()).astype(np.float32),
            affine=data_tx_rigid.affine,
        )

        nib.save(data_tx_rigid, f"{OUTPUT_RIGID_FULL_PATH}/{opath}")
        data_tx_rigid_half = processing.conform(
            data_tx_rigid, out_shape=(80, 112, 80), voxel_size=(2.0, 2.0, 2.0), order=1
        )
        nib.save(data_tx_rigid_half, f"{OUTPUT_RIGID_HALF_PATH}/{opath}")
        
        ### TRSAA ###
        tx = ants.registration(mni_ants, data_ants, type_of_transform="TRSAA")
        data_tx_trsaa = nib.as_closest_canonical(ants.to_nibabel(tx["warpedmovout"]))
        data_mask_tx_trsaa = nib.as_closest_canonical(
            ants.to_nibabel(
                ants.apply_transforms(
                    fixed=mni_ants,
                    moving=mask_ants,
                    transformlist=tx["fwdtransforms"],
                    interpolator="nearestNeighbor",
                )
            )
        )
        data_tx_trsaa = nib.Nifti1Image(
            (data_tx_trsaa.get_fdata() * data_mask_tx_trsaa.get_fdata()).astype(np.float32),
            affine=data_tx_trsaa.affine,
        )

        nib.save(data_tx_trsaa, f"{OUTPUT_TRSAA_FULL_PATH}/{opath}")
        data_tx_trsaa_half = processing.conform(
            data_tx_trsaa, out_shape=(80, 112, 80), voxel_size=(2.0, 2.0, 2.0), order=1
        )
        nib.save(data_tx_trsaa_half, f"{OUTPUT_TRSAA_HALF_PATH}/{opath}")
        

if __name__ == "__main__":
    main()