import mne

cd ~/Data/epilepsy/b134b/2
raw = mne.io.Raw('hb,lf-raw.fif')
events = mne.read_events('epi-eve.fif')
# event_id = dict(quiet=1,rythm=2,hf=3)
event_id = dict(hf=3)
epochsHF = mne.Epochs(raw, events, event_id,
                    tmin=0, tmax=0.5, baseline=(None, None), preload=True)
event_id = dict(BL=1)
epochsBL = mne.Epochs(raw, events, event_id,
                    tmin=0, tmax=0.5, baseline=(None, None), preload=True)
epochsBL.pick_types('mag')
epochsBL.plot_psd_topomap()
BLpsd, freqs = mne.time_frequency.compute_epochs_psd(epochsBL,
                    fmin=2, fmax=100, n_fft=501, n_jobs=4)
average_psds = BLpsd.mean(0)
# http://nullege.com/codes/show/src%40m%40n%40mne-0.7.1%40examples%40time_frequency%40plot_single_trial_spectra.py/23/mne.time_frequency.compute_epochs_psd/python
fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(10, 5))
fig.suptitle('Single trial power', fontsize=12)
ax1.imshow(some_psds[:, freq_mask].T, aspect='auto', origin='lower')

