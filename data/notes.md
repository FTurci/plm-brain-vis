## Data structure


### plm_model.npy

This .npy file contains the PLM model inferred from the entire multi-participant human connectome project (HCP) dataset supplied by Ryota.

- Shape (360, 360), symmetric matrix of interactions between regions i and j. Diagonals contain hi's and off diagonals are Jij's.

### mc_data.npy

This is an example dataset containing configurations generated from monte carlo simulations of the model found in plm-model.npy.

- Shape (12, 10000, 360), 12 independent repeat simulations of the same model, generating a trajecotry of shape (10000, 360) containing B=10000 samples of the N=360 spins.

## ROIname.txt

Labels of the segmented brain regions of interest. Only 180 labels are in this file as the regions in the left and right hemispheres have the same label. I.e. ROI 0 = left-V1, ROI 180 = right-V1.
