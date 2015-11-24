import mne


# cd ~/Data/marik/yuval/3

# read the data and write as fif
raw = mne.io.bti.read_raw_bti(
    'xc,hb,lf_c,rfhp0.1Hz', rename_channels=False, sort_by_ch_name=False)
raw.pick_types(meg=True)
raw.save('som-raw.fif')
# filter
raw = mne.io.read_raw_fif('som-raw.fif', preload=True,)
raw.filter(1, 20)
# make epochs and compute noise covariance
events = mne.read_events('som-eve.fif')
event_id = dict(handR=2,handL=4)
epochs = mne.Epochs(raw, events, event_id, tmin=-0.1,
                    tmax=0.3, baseline=(None, 0), preload=True)
noise_cov = mne.compute_covariance(
    epochs, tmax=0., method='empirical')
mne.write_cov('BL-cov.fif',noise_cov)
data_cov = mne.compute_covariance(epochs, method='empirical')
mne.write_cov('all-cov.fif',data_cov)

handR = epochs['handR'].average()
handL = epochs['handL'].average()
handLR=handL.copy()
handLR.data=handL.data+handR.data
# butterfly plot
handLR.plot()
# topography plot
handLR.plot_topomap(times=(0.05))
handL.save('handL-ave.fif')
handR.save('handR-ave.fif')
handLR.save('handLR-ave.fif')
