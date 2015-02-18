import mne
raw=mne.io.Raw('odelia-raw.fif');
events = mne.find_events(raw, stim_channel='STI 014')
event_id = 202  # the event number in events
tmin = -0.25  # start of each epoch (200ms before the trigger)
tmax = 0.55  # end of each epoch (500ms after the trigget)
picks = mne.fiff.pick_types(raw.info, meg=True, eeg=False, eog=False)
baseline = (None, 0)
reject = dict(mag=4e-12)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,picks=picks, baseline=baseline, preload=True,reject=reject)
epochs_data = epochs.get_data()
evoked = epochs.average()
# plot
from mne.viz import plot_evoked
plot_evoked(evoked)
# save
evoked.save('sagitf_evoked.fif')
# cov
cov = mne.compute_covariance(epochs, tmin=None, tmax=0)
cov.save('sagitf_raw-cov.fif')
# below is shell, not python
ln -s /usr/local/freesurfer/subjects/Sagit/bem/watershed/Sagit_inner_skull_surface /usr/local/freesurfer/subjects/Sagit/bem/Sagit-inner_skull.surf
mne_setup_source_space --ico -6 --overwrite
mne_setup_forward_model --homog --surf --ico 4 --overwrite
MEG_FN='sagitf_raw.fif'
mne_do_forward_solution --spacing oct-6 mindist --overwrite --meas $MEG_FN --megonly --noisecov 
mne_do_inverse_operator --fwd sagitf_raw-oct-6-fwd.fif --deep --loose 0.2 --meg

