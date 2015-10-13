__author__ = 'yuval'
# this is step 5 in Inbal4.py
import mne
from mne.viz import plot_evoked
# I used matlab mne_write_events to write the -eve.fiff file as explained in the docs/*.pptx
events = mne.read_events('4-eve.fif')
raw=mne.io.Raw('4_raw.fif',preload=True);
raw.filter(1,40)
event_id = 100
tmin = -0.3  # start of each epoch (200ms before the trigger)
tmax = 0.7  # end of each epoch (500ms after the trigget)
picks = mne.pick_types(raw.info, meg=True, eeg=False, eog=False)
baseline = (None, 0)
#reject = dict(mag=4e-12)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,picks=picks, baseline=baseline, preload=True)
epochs_data = epochs.get_data()
evoked = epochs.average()
# plot

plot_evoked(evoked)
# save
# evoked.save('MNE/'+folder+'_wbw-ave.fif')
cov = mne.compute_covariance(epochs, tmin=-0.2, tmax=0)
cov.save('4AudBL-cov.fif')


