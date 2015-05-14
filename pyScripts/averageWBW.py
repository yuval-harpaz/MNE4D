
import os
_, folder = os.path.split(os.getcwd())

import mne
raw=mne.io.Raw('MNE/'+folder+'_raw.fif',preload='true');
raw.filter(1,40)
events = mne.read_events('MNE/wbw-eve.fif')
event_id = 2048  # the event number in events
tmin = -0.5  # start of each epoch (200ms before the trigger)
tmax = 0.8  # end of each epoch (500ms after the trigget)
picks = mne.pick_types(raw.info, meg=True, eeg=False, eog=False)
baseline = (-0.2, 0)
#reject = dict(mag=4e-12)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,picks=picks, baseline=baseline, preload=True)
epochs_data = epochs.get_data()
evoked = epochs.average()
# plot
#from mne.viz import plot_evoked
#plot_evoked(evoked)
# save
evoked.save('MNE/'+folder+'_wbw-ave.fif')
# cov
cov = mne.compute_covariance(epochs, tmin=-0.2, tmax=0)
cov.save('MNE/'+folder+'_wbw-cov.fif')
# below is shell, not python
# mne_watershed_bem --atlas --overwrite --subject aliceYoni
# ln -s /usr/local/freesurfer/subjects/aliceYoni/bem/watershed/aliceYoni_inner_skull_surface /usr/local/freesurfer/subjects/aliceYoni/bem/aliceYoni-inner_skull.surf
#mne_setup_source_space --ico -6 --overwrite
#mne_setup_source_space --subject aliceYoni --ico -6 --overwrite
#mne_setup_forward_model --subject aliceYoni --homog --surf --ico 4 --overwrite
#MEG_FN=folder+'_raw.fif'
# for this stage you have to have a -trans.fif file, use mne_analyze to load digitization points and headshape, nudge headshape to MRI and save the -trans file.
#mne_do_forward_solution --spacing oct-6 mindist --overwrite --meas $MEG_FN --megonly --noisecov 
#mne_do_inverse_operator --fwd yoni_raw-oct-6-fwd.fif --deep --loose 0.2 --meg --noisecov yoni_wbw-cov.fif

