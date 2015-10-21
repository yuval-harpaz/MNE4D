#!/usr/bin/env bash
# 1. convert data
4D2fiff
# mne_bti2fiff.py -p rs,xc,hb,lf_c,rfhp0.1Hz -o 4_raw.fif

# 2. watershed, make a surface from the headshape (14min)
export SUBJECT=inbal4
mne_watershed_bem --atlas
ln -s /usr/local/freesurfer/subjects/${SUBJECT}/bem/watershed/${SUBJECT}_inner_skull_surface /usr/local/freesurfer/subjects/${SUBJECT}/bem/${SUBJECT}-inner_skull.surf

# 3. setup MRI space
mne_setup_mri --overwrite

# 4. align MRI to headshape
mne_analyze &
# follow the instructions on MNE4D/docs/MNE_4D_data.pptx

# 5. compute noise covariance
# see inbal4.py

# 6. compute forward and inverse solutions
mne_setup_source_space --ico -6 --overwrite
mne_setup_forward_model --homog --surf --ico 4 --overwrite
mne_do_forward_solution --spacing oct-6 --overwrite --meas 4_raw.fif --megonly --noisecov
mne_do_inverse_operator --fwd 4_raw-oct-6-fwd.fif --deep --loose 0.2 --meg --noisecov 4AudBL-cov.fif

# from here we go on in python, get back to inbal4.py

# for inbal4temp (Colin 27)

mne_do_forward_solution --spacing oct-6 --fwd 4temp --meas 4_raw.fif --megonly --noisecov
mne_do_inverse_operator --fwd 4temp-fwd.fif --deep --loose 0.2 --meg --noisecov 4AudBL-cov.fif