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
# BL_cov = mne.compute_covariance(epochsBL, tmax=0.5, method='empirical')
# BL_cov.save('empirical_BL-cov.fif')
# fig_cov, fig_spectra = mne.viz.plot_cov(BL_cov, raw.info)
fwd=mne.read_forward_solution('b134-fwd.fif')
fwd=mne.convert_forward_solution(fwd,surf_ori=True)
# DICS
hf_csds = mne.time_frequency.compute_epochs_csd(epochsHF, mode='multitaper', tmin=0, tmax=0.5,
                               fmin=20, fmax=40, fsum=False)
bl_csds = mne.time_frequency.compute_epochs_csd(epochsBL, mode='multitaper', tmin=0, tmax=0.5,
                               fmin=20, fmax=40, fsum=False)
# Compute DICS spatial filter and estimate source power
stc = mne.beamformer.dics_source_power(epochsHF.info, fwd, bl_csds, hf_csds, pick_ori='normal')
%gui
%gui wx
brain = stc.plot(surface='pial', hemi='both', time_viewer=True, )

clim = dict(kind='value', lims=[0, 5, 10])
i=4
brain = stc.plot(surface='inflated', hemi='both', time_label= '%0.1f Hz' %data_csds[i].frequencies, clim=clim)
brain.set_data_time_index(i)

rawE = mne.io.Raw('/home/yuval/Data/emptyRoom/lf_raw.fif')
events = mne.read_events('/home/yuval/Data/emptyRoom/1s-eve.fif')
# event_id = dict(quiet=1,rythm=2,hf=3)
event_id = dict(empty=1)
epochsE = mne.Epochs(rawE, events, event_id,
                    tmin=0, tmax=0.5, baseline=(None, None), preload=True)
empty_csds = mne.time_frequency.compute_epochs_csd(epochsE, mode='multitaper', tmin=0, tmax=0.5,
                               fmin=20, fmax=40, fsum=False)
stcBL_E = mne.beamformer.dics_source_power(epochsHF.info, fwd, empty_csds, bl_csds, pick_ori='normal')
clim = dict(kind='value', lims=[0, 25, 50])
i=5
brain = stcBL_E.plot(surface='inflated', hemi='both', time_label= '%0.1f Hz' %data_csds[i].frequencies, clim=clim)
brain.set_data_time_index(i)

### dSPM
invBL=mne.minimum_norm.read_inverse_operator('BL-inv.fif')
snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"

stcHF = mne.minimum_norm.compute_source_psd_epochs(epochsHF,invBL,lambda2, method, fmin=20, fmax=40)
stcHFavg=stc.copy()
stcHFavg.lh_data[:]=0
stcHFavg.rh_data[:]=0
for i in range(0,27):
    stcHFavg.lh_data[:]=stcHFavg.lh_data+stcHF[i].lh_data
    stcHFavg.rh_data[:]=stcHFavg.rh_data+stcHF[i].rh_data

stcHFavg.rh_data[:]=stcHFavg.rh_data[:]/27
stcHFavg.lh_data[:]=stcHFavg.lh_data[:]/27
clim = dict(kind='value', lims=[0, 50, 100])
i=4
brain = stcHFavg.plot(surface='inflated', hemi='both', time_label= '%0.1f Hz' %data_csds[i].frequencies, clim=clim)
brain.set_data_time_index(i)
clim = dict(kind='value', lims=[0, 150, 300])
i=0
brain = stcHFavg.plot(surface='inflated', hemi='both', time_label= '%0.1f Hz' %data_csds[i].frequencies, clim=clim)
brain.set_data_time_index(i)
clim = dict(kind='value', lims=[0, 50, 100])
i=9
brain = stcHFavg.plot(surface='inflated', hemi='both', time_label= '%0.1f Hz' %data_csds[i].frequencies, clim=clim)
brain.set_data_time_index(i)

invE=mne.minimum_norm.read_inverse_operator('Empty-inv.fif')
stcBL = mne.minimum_norm.compute_source_psd_epochs(epochsBL,invE,lambda2, method, fmin=20, fmax=40)
stcBLavg=stc.copy()
stcBLavg.lh_data[:]=0
stcBLavg.rh_data[:]=0
for i in range(0,len(stcBL)):
    stcBLavg.lh_data[:]=stcBLavg.lh_data+stcBL[i].lh_data
    stcBLavg.rh_data[:]=stcBLavg.rh_data+stcBL[i].rh_data

stcBLavg.rh_data[:]=stcBLavg.rh_data[:]/len(stcBL)
stcBLavg.lh_data[:]=stcBLavg.lh_data[:]/len(stcBL)
clim = dict(kind='value', lims=[0, 5, 10])
i=0
brain = stcBLavg.plot(surface='white', hemi='both', time_label= '%0.1f Hz' %data_csds[i].frequencies, clim=clim)
brain.set_data_time_index(i)
