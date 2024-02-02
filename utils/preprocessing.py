import SimpleITK as sitk

def N4_Bias_Field_Correction(input_path, output_path):
    raw_img_sitk = sitk.ReadImage(input_path, sitk.sitkFloat32)
    transformed = sitk.RescaleIntensity(raw_img_sitk, 0, 255)
    transformed = sitk.LiThreshold(transformed, 0, 1)
    head_mask = transformed
    shrinkFactor = 4
    inputImage = sitk.Shrink(raw_img_sitk, [shrinkFactor] * raw_img_sitk.GetDimension())
    maskImage = sitk.Shrink(head_mask, [shrinkFactor] * raw_img_sitk.GetDimension())
    bias_corrector = sitk.N4BiasFieldCorrectionImageFilter()
    corrected = bias_corrector.Execute(inputImage, maskImage)
    log_bias_field = bias_corrector.GetLogBiasFieldAsImage(raw_img_sitk)
    corrected_image_full_resolution = raw_img_sitk / sitk.Exp(log_bias_field)
    sitk.WriteImage(corrected_image_full_resolution, output_path)
    return