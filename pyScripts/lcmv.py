# ipython --gui=wx
import os
from mne.beamformer import lcmv
import mne
from surfer import Brain
import numpy as np
_, folder = os.path.split(os.getcwd())
raw=mne.io.Raw('MNE/'+folder+'_raw.fif',preload='true');
raw.filter(1,40)
events = mne.read_events('MNE/nat-eve.fif')
event_id = 100  # the event number in events
tmin = -0.6  # start of each epoch (200ms before the trigger)
tmax = 0.5  # end of each epoch (500ms after the trigget)
picks = mne.pick_types(raw.info, meg=True, eeg=False, eog=False)
baseline = (-0.6, -0.4)
#reject = dict(mag=4e-12)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,picks=picks, baseline=baseline, preload=True)
#evoked=mne.read_evokeds('MNE/nat-ave.fif')
evoked1 = epochs.average()
noise_cov = mne.read_cov('/home/yuval/Data/emptyRoom/empty-cov.fif')
data_cov = mne.compute_covariance(epochs, tmin=0.04, tmax=0.15) #method='shrunk'
forward = mne.read_forward_solution('MNE/'+folder+'_raw-oct-6-fwd.fif')

# Read regularized noise covariance and compute regularized data covariance
#plt.close('all')
#pick_oris = [None, 'normal', 'max-power']
#names = ['free', 'normal', 'max-power']

vertices=np.arange(10242)
stc = lcmv(evoked1, forward, noise_cov, data_cov, reg=0.01)
# stcF = lcmv(evoked1, fwdFixed, noise_cov, data_cov, reg=0.01,pick_ori='normal')
stc_to = mne.morph_data('aliceIdan', 'fsaverage', stc, n_jobs=4, grade=[vertices,vertices])
data = stc_to.data[:,712]
brain = Brain('fsaverage', 'both', 'inflated', views='caudal')
brain.add_data(data[0:10242], colormap='hot', vertices=vertices, smoothing_steps=10, hemi='lh')
brain.add_data(data[10242:], colormap='hot', vertices=vertices, smoothing_steps=10, hemi='rh') 
maxT=data.max()
brain.scale_data_colormap(fmin=0, fmid=maxT/2, fmax=maxT, transparent=True)
# mne_do_forward_solution --spacing oct-6 mindist --meas idan_raw.fif --megonly --noisecov --fixed --fwd fixed-fwd.fif
fwdFixed=mne.read_forward_solution('MNE/fixed-fwd.fif')
stcF = lcmv(evoked1, fwdFixed, noise_cov, data_cov, reg=0.01)
data = stcF.data[:,712]
brain = Brain('aliceIdan', 'both', 'inflated', views='ventral')
brain.add_data(data[0:4098], colormap='hot', vertices=stcF.vertices[0], smoothing_steps=10, hemi='lh')
brain.add_data(data[4098:], colormap='hot', vertices=stcF.vertices[1], smoothing_steps=10, hemi='rh') 
maxT=data.max()
brain.scale_data_colormap(fmin=0, fmid=maxT/2, fmax=maxT, transparent=True)

data = stc.data[:,712]
brain = Brain('aliceIdan', 'both', 'inflated', views='ventral')
brain.add_data(data[0:4098], colormap='hot', vertices=stc.vertices[0], smoothing_steps=10, hemi='lh')
brain.add_data(data[4098:], colormap='hot', vertices=stc.vertices[1], smoothing_steps=10, hemi='rh') 
#maxT=data.max()
brain.scale_data_colormap(fmin=0, fmid=maxT/2, fmax=maxT, transparent=True)


