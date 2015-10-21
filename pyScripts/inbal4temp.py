__author__ = 'yuval'
# this is step 5 in Inbal4.py
import mne
import numpy as np
import surfer
import pickle

cd ~/Data/inbal/4
evoked = mne.read_evokeds('4aud-ave.fif', condition=0, baseline=(-0.2, 0))
#inverse_operator = mne.minimum_norm.read_inverse_operator('4_raw-oct-6-meg-inv.fif')
inverse_operator = mne.minimum_norm.read_inverse_operator('4temp-meg-inv.fif')
snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"
stc = mne.minimum_norm.apply_inverse(evoked, inverse_operator, lambda2, method, pick_ori=None)
stc.save('4tempaud_dSPM')

# plot the subject's brain with pysurfer
% gui
% gui wx


# adding functional data
stcR = surfer.io.read_stc('4tempaud_dSPM-rh.stc')
dataR = stcR['data']
verticesR = stcR['vertices']
stcL = surfer.io.read_stc('4tempaud_dSPM-lh.stc')
dataL = stcL['data']
verticesL = stcL['vertices']
time = 1e3 * np.linspace(stcL['tmin'], stcL['tmin'] + dataL.shape[1] * stcL['tstep'], dataL.shape[1])
colormap = 'hot'
time_label = 'time=%0.2f ms'
# export SUBJECTS_DIR=/usr/local/freesurfer/subjects/
brain = surfer.Brain('inbal4temp', 'both', 'white', views='caudal',subjects_dir='/usr/local/freesurfer/subjects/')
brain.add_data(dataL, colormap=colormap, vertices=verticesL, smoothing_steps=10, time=time, time_label=time_label, hemi='lh')
brain.add_data(dataR, colormap=colormap, vertices=verticesR, smoothing_steps=10, time=time, time_label=time_label, hemi='rh')
brain.set_data_time_index(388)
brain.scale_data_colormap(fmin=0, fmid=10, fmax=20, transparent=True)
viewer = surfer.TimeViewer(brain)

brain.set_data_time_index(433)


# morph, move to data to fsaverage (Talairach)
# make the transformation matrix. this takes a few min, save for later use.
vertices_to = [np.arange(10242), np.arange(10242)]
morph_mat = mne.compute_morph_matrix('inbal4', 'fsaverage', stc.vertno, vertices_to, subjects_dir='/usr/local/freesurfer/subjects')
print("done morphing")
pickle.dump(morph_mat,open('morph_mat.p','w'))
# you can read it like this:
# morph_mat = pickle.load( open( "morph_mat.p", "rb" ) )
stc_fsa = mne.morph_data_precomputed('inbal4', 'fsaverage', stc, vertices_to, morph_mat)


dataL = stc_fsa.lh_data
dataR = stc_fsa.rh_data
verticesL = stc_fsa.lh_vertno;
verticesR = stc_fsa.rh_vertno;

time = 1e3 * np.linspace(stcL['tmin'], stcL['tmin'] + dataL.shape[1] * stcL['tstep'], dataL.shape[1])
colormap = 'hot'
time_label = 'time=%0.2f ms'
# export SUBJECTS_DIR=/usr/local/freesurfer/subjects/
brain = surfer.Brain('fsaverage', 'both', 'pial', views='caudal',subjects_dir='/usr/local/freesurfer/subjects/')
brain.add_data(dataL, colormap=colormap, vertices=verticesL, smoothing_steps=10, time=time, time_label=time_label, hemi='lh')
brain.add_data(dataR, colormap=colormap, vertices=verticesR, smoothing_steps=10, time=time, time_label=time_label, hemi='rh')
brain.set_data_time_index(388)
brain.scale_data_colormap(fmin=0, fmid=4, fmax=8, transparent=True)
viewer = surfer.TimeViewer(brain)

brain.set_data_time_index(433)