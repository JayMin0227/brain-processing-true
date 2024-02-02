import os
import torch
from utils.network import UNet

def load_model(device):
    CNET_MODEL_PATH = "/data2/radiology_datas/clean3/OpenMAP-T1/V2/CNet/CNet.pth"
    SSNET_MODEL_PATH = "/data2/radiology_datas/clean3/OpenMAP-T1/V2/SSNet/SSNet.pth"
    PNETC_MODEL_PATH = "/data2/radiology_datas/clean3/OpenMAP-T1/V2/PNet/coronal.pth"
    PNETS_MODEL_PATH = "/data2/radiology_datas/clean3/OpenMAP-T1/V2/PNet/sagittal.pth"
    PNETA_MODEL_PATH = "/data2/radiology_datas/clean3/OpenMAP-T1/V2/PNet/axial.pth"
    HNETC_MODEL_PATH = "/data2/radiology_datas/clean3/OpenMAP-T1/V2/HNet/coronal.pth"
    HNETA_MODEL_PATH = "/data2/radiology_datas/clean3/OpenMAP-T1/V2/HNet/axial.pth"

    cnet = UNet(1, 1)
    cnet.load_state_dict(torch.load(CNET_MODEL_PATH))
    cnet.to(device)
    cnet.eval()

    ssnet = UNet(1, 1)
    ssnet.load_state_dict(torch.load(SSNET_MODEL_PATH))
    ssnet.to(device)
    ssnet.eval()

    pnet_c = UNet(3, 142)
    pnet_c.load_state_dict(torch.load(PNETC_MODEL_PATH))
    pnet_c.to(device)
    pnet_c.eval()

    pnet_s = UNet(3, 142)
    pnet_s.load_state_dict(torch.load(PNETS_MODEL_PATH))
    pnet_s.to(device)
    pnet_s.eval()

    pnet_a = UNet(3, 142)
    pnet_a.load_state_dict(torch.load(PNETA_MODEL_PATH))
    pnet_a.to(device)
    pnet_a.eval()

    hnet_c = UNet(1, 3)
    hnet_c.load_state_dict(torch.load(HNETC_MODEL_PATH))
    hnet_c.to(device)
    hnet_c.eval()

    hnet_a = UNet(1, 3)
    hnet_a.load_state_dict(torch.load(HNETA_MODEL_PATH))
    hnet_a.to(device)
    hnet_a.eval()
    return cnet, ssnet, pnet_c, pnet_s, pnet_a, hnet_c, hnet_a