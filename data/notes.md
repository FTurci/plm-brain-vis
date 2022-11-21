## Data structure


### plm_model.npy

This .npy file contains the PLM model inferred from the entire multi-participant human connectome project (HCP) dataset supplied by Ryota.

- Shape (360, 360), symmetric matrix of interactions between regions i and j. Diagonals contain hi's and off diagonals are Jij's.

### mc_data.npy

This is an example dataset containing configurations generated from monte carlo simulations of the model found in plm-model.npy.

- Shape (12, 10000, 360), 12 independent repeat simulations of the same model, generating a trajecotry of shape (10000, 360) containing B=10000 samples of the N=360 spins.

## ROIname.txt

Labels of the segmented brain regions of interest. Only 180 labels are in this file as the regions in the left and right hemispheres have the same label. I.e. ROI 0 = left-V1, ROI 180 = right-V1.

## roi_clusters.csv

A csv which allows you to map the roi_index (a number between 0-179 inclusive) to the roi_name.
The ROIs can also be grouped into clusters which are "grouped by geographic	proximity and functional similarities", see https://static-content.springer.com/esm/art%3A10.1038%2Fnature18933/MediaObjects/41586_2016_BFnature18933_MOESM330_ESM.pdf.

There are 22 clusters. Each of these clusters has a type, roughly according to it's function, e.g. 'Visual' or 'Auditory'. There are 5 types. See ../code/cluster_selection_demo.py for a demo how to sub-set the inferred model by these clusters and types.