# ipython --gui=wx
from os import chdir as cd
from mne.beamformer import lcmv
import mne

subjects = ['idan', 'inbal', 'liron', 'maor', 'mark', 'ohad', 'odelia', 'yoni'];
for sub in subjects:
    #X=[]
    fsSub='alice'+sub[0].upper()+sub[1:]
    cd('/home/yuval/Copy/MEGdata/alice/'+sub+'/MNE')
    raw=mne.io.Raw(sub+'_raw.fif',preload='true');
    raw.filter(1,40)
    events = mne.read_events('nat-eve.fif')
    event_id = 100  # the event number in events
    tmin = -0.6  # start of each epoch (200ms before the trigger)
    tmax = 0.5  # end of each epoch (500ms after the trigget)
    picks = mne.pick_types(raw.info, meg=True, eeg=False, eog=False)
    baseline = (-0.6, -0.4)
    #reject = dict(mag=4e-12)
    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,picks=picks, baseline=baseline, preload=True)
    evoked=mne.read_evokeds('nat-ave.fif')
    evoked1 = epochs.average()
    noise_cov = mne.read_cov('/home/yuval/Data/emptyRoom/empty-cov.fif')
    data_cov = mne.compute_covariance(epochs, tmin=0.04, tmax=0.15) #method='shrunk'
    forward = mne.read_forward_solution(sub+'_raw-oct-6-fwd.fif')
    stc_orig = lcmv(evoked[0], forward, noise_cov, data_cov, reg=0.01)
    stc_orig.save('lcmv_orig')

