import mne
import numpy as np
cd /media/yuval/win_disk/Data/connectomeDB/MEG/917255/unprocessed/MEG/3-Restin/4D
raw = mne.io.bti.read_raw_bti('c,rfDC',head_shape_fname=None,preload=True)
raw.save('917255_raw.fif')
ecg_events, _, _ = mne.preprocessing.find_ecg_events(raw,ch_name='EEG 001')
mne.write_events('917255_ecg-eve.fif', ecg_events)

## compute PCA

proj=mne.preprocessing.compute_proj_ecg(raw, raw_event=None, tmin=-0.1, tmax=0.1,ch_name='EEG 001',
                n_mag=2, n_eeg=0, l_freq=1.0, h_freq=35.0,
                average=False, filter_length='10s', n_jobs=4,
                reject={'mag': 3e-12}, flat=None, bads=[], no_proj=False,
                event_id=999, copy=True, verbose=None)
mne.write_proj('917255_proj.fif',proj[0])

## apply proj
raw=mne.io.Raw('917255_raw.fif',preload=True)
proj=mne.read_proj('917255_proj.fif')

raw.add_proj(proj[1])
raw.plot_projs_topomap()

raw.apply_proj()
raw.save('917255_proj_raw.fif')
