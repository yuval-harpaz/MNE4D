__author__ = 'yuval'
# this is step 5 in Inbal4.py
import mne
import numpy as np
import surfer
import pickle
# I used matlab mne_write_events to write the -eve.fiff file as explained in the docs/*.pptx
events = mne.read_events('4-eve.fif')
raw=mne.io.Raw('4_raw.fif',preload=True);
raw.filter(1,40)
print('done filtering')
event_id = 100
tmin = -0.3  # start of each epoch (200ms before the trigger)
tmax = 0.7  # end of each epoch (500ms after the trigget)
picks = mne.pick_types(raw.info, meg=True, eeg=False, eog=False)
baseline = (None, 0)
#reject = dict(mag=4e-12)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,picks=picks, baseline=baseline, preload=True)
epochs_data = epochs.get_data()
evoked = epochs.average()
# to implant data cleaned with fieldtrip into the matrix see averageConds.py
evoked.save('4aud-ave.fif')
# plot
mne.viz.plot_evoked(evoked)

cov = mne.compute_covariance(epochs, tmin=-0.2, tmax=0)
cov.save('4AudBL-cov.fif')

# dSPM source localization
snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)

#evoked = mne.read_evokeds('4aud-ave.fif', condition=0, baseline=(-0.2, 0))
inverse_operator = mne.minimum_norm.read_inverse_operator('4_raw-oct-6-meg-inv.fif')
stc = mne.minimum_norm.apply_inverse(evoked, inverse_operator, lambda2, method, pick_ori=None)
stc.save('4aud_dSPM')

# plot the subject's brain with pysurfer
% gui
% gui wx


# adding functional data
stcR = surfer.io.read_stc('4aud_dSPM-rh.stc')
dataR = stcR['data']
verticesR = stcR['vertices']
stcL = surfer.io.read_stc('4aud_dSPM-lh.stc')
dataL = stcL['data']
verticesL = stcL['vertices']
time = 1e3 * np.linspace(stcL['tmin'], stcL['tmin'] + dataL.shape[1] * stcL['tstep'], dataL.shape[1])
colormap = 'hot'
time_label = 'time=%0.2f ms'
# export SUBJECTS_DIR=/usr/local/freesurfer/subjects/
brain = surfer.Brain('inbal4', 'both', 'white', views='caudal',subjects_dir='/usr/local/freesurfer/subjects/')
brain.add_data(dataL, colormap=colormap, vertices=verticesL, smoothing_steps=10, time=time, time_label=time_label, hemi='lh')
brain.add_data(dataR, colormap=colormap, vertices=verticesR, smoothing_steps=10, time=time, time_label=time_label, hemi='rh')
brain.set_data_time_index(388)
brain.scale_data_colormap(fmin=0, fmid=4, fmax=8, transparent=True)
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