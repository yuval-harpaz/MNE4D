import scipy.io
from os import chdir
import mne

chdir('/home/yuval/Copy/MEGdata/alice/ga2015')
# matlab: Nat is avgMr.individual from GavgEqTrl.mat
mat = scipy.io.loadmat('Nat.mat')
mat=mat['Nat']
subjects = ['idan', 'inbal', 'liron', 'maor', 'mark', 'ohad', 'odelia', 'yoni'];
counter=0
events = mne.read_events('/home/yuval/Copy/MEGdata/alice/stum-eve.fif')
chanInd=np.array([186,2,46,148,57,150,218,15,14,50,42,66,34,152,154,19,223,224,118,12,120,1,219,85,39,8,101,32,172,162,62,125,188,222,21,159,23,81,10,182,216,87,111,246,74,214,43,241,139,71,206,196,200,133,124,91,89,128,158,129,149,119,48,45,13,86,52,143,176,40,7,41,202,171,105,70,208,60,131,97,166,28,220,122,126,90,192,130,193,217,83,215,9,153,16,88,178,38,76,110,180,113,136,3,68,239,108,165,163,233,234,26,100,17,53,92,190,227,195,95,147,117,183,181,11,151,51,142,209,109,210,114,244,247,103,204,102,5,138,230,94,197,99,231,135,127,189,191,226,156,93,229,184,221,49,141,177,245,144,44,146,238,137,173,35,140,104,61,132,24,167,164,169,55,18,59,47,185,187,75,80,213,115,205,236,67,240,72,96,199,22,201,155,56,161,243,212,211,116,112,170,30,134,36,174,107,25,228,232,98,198,84,123,6,78,248,179,168,65,31,242,69,63,27,160,203,157,20,121,82,73,175,37,77,79,145,207,29,33,106,4,58,194,235,64,237,54,225,])
chanInd=chanInd-1
for sub in subjects:
    chdir('/home/yuval/Copy/MEGdata/alice/'+sub+'/MNE')
    raw=mne.io.Raw(sub+'_raw.fif');
    event_id = 2  # the event number in events
    tmin = -0.6  # start of each epoch (200ms before the trigger)
    tmax = 0.601  # end of each epoch (500ms after the trigget)
    picks = mne.pick_types(raw.info, meg=True, eeg=False, eog=False)
    baseline = (-0.2, 0)
    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,picks=picks, baseline=baseline, preload=True)
    epochs_data = epochs.get_data()
    evoked = epochs.average()
    evoked.data=mat[counter,chanInd,:]
    evoked.save('nat-ave.fif')
    counter+=1
    print('done '+sub)

