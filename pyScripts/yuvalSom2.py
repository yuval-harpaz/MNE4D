import mne
from shutil import copyfile
subject = 'yuval'
freesurfer_home = "/usr/local/freesurfer"
subjects_dir = freesurfer_home + "/subjects"

# environ["FREESURFER_HOME"] = freesurfer_home
# environ["subject"] = subject
# mne_bin = "/home/yuval/Programs/MNE-2.7.3-3268-Linux-x86_64/bin"
# path = environ['PATH']
# path = path + ":" + freesurfer_home + "/bin:" + mne_bin
# environ['PATH'] = path
# ld_lib = environ['LD_LIBRARY_PATH']
# ld_lib = ld_lib + ":" + freesurfer_home + "/lib"
# environ['LD_LIBRARY_PATH'] = ld_lib
#


# watershed - make BEM model with freesurfer
ws = mne.bem.make_watershed_bem(
    subject=subject, subjects_dir=subjects_dir, overwrite=True)
copyfile(subjects_dir + "/" + subject + "/bem/watershed/" + subject +
         "_inner_skull_surface", subjects_dir + "/" + subject + "/bem/inner_skull.surf")

# cd ~/Data/marik/yuval/3


bem_model = mne.make_bem_model(
    subject=subject, subjects_dir=subjects_dir, conductivity=(0.3,))
bem_solution = mne.make_bem_solution(bem_model)
# /usr/local/freesurfer/subjects/aliceIdan/bem
mne.write_bem_solution(
    subjects_dir + "/" + subject + "/bem/" + subject + "-bem.fif", bem_solution)

# mark fiducials in the GUI, nudge and save
mne.gui.coregistration(
    subject=subject, subjects_dir=subjects_dir, inst='som-raw.fif')

src = mne.setup_source_space(
    subject, subjects_dir=subjects_dir, add_dist=False, overwrite=True)
trans = 'yuval-trans.fif'
bem = subjects_dir + '/' + subject + '/bem/' + subject + '-bem.fif'

# Note that forward solutions can also be read with read_forward_solution
raw = mne.io.Raw('som-raw.fif')
fwd = mne.make_forward_solution(
    raw.info, trans, src, bem, fname='som-fwd.fif', meg=True, eeg=False, mindist=5.0, n_jobs=4, overwrite=True)

noise_cov=mne.read_cov('BL-cov.fif')
inv = mne.minimum_norm.make_inverse_operator(raw.info, fwd, noise_cov)
mne.minimum_norm.write_inverse_operator('som-inv.fif', inv)
fwdFixed = mne.convert_forward_solution(fwd, surf_ori=True)
invFixed = mne.minimum_norm.make_inverse_operator(raw.info, fwdFixed, noise_cov, fixed=True)
mne.minimum_norm.write_inverse_operator('somFixed-inv.fif', invFixed)

handL=mne.read_evokeds('handL-ave.fif')
handL=handL[0]
handL.plot()
snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"
stcHL = mne.minimum_norm.apply_inverse(handL, inv, lambda2, method, pick_ori=None)
%gui
%gui wx

clim = dict(kind='value', lims=[5, 10, 25])
i=150
stcHLfixed = mne.minimum_norm.apply_inverse(handL, invFixed, lambda2, method, pick_ori=None)



handR=mne.read_evokeds('handR-ave.fif')
handR=handR[0]
stcHRfixed = mne.minimum_norm.apply_inverse(handR, invFixed, lambda2, method, pick_ori=None)



handLR=mne.read_evokeds('handLR-ave.fif')
handLR=handLR[0]
stcHLRfixed = mne.minimum_norm.apply_inverse(handLR, invFixed, lambda2, method, pick_ori=None)

brain = stcHLfixed.plot(subject=subject, surface='white', hemi='both', colormap='hot',
        smoothing_steps=5, transparent=True, subjects_dir=subjects_dir, time_viewer=False,
        clim=clim, figure=0)
brain.set_data_time_index(150)
brainR = stcHRfixed.plot(subject=subject, surface='white', hemi='both', colormap='hot',
        smoothing_steps=5, transparent=True, subjects_dir=subjects_dir, time_viewer=False,
        clim=clim, figure=1)
brainR.set_data_time_index(150)
brainLR = stcHLRfixed.plot(subject=subject, surface='white', hemi='both', colormap='hot',
        smoothing_steps=5, transparent=True, subjects_dir=subjects_dir, time_viewer=False,
        clim=clim, figure=None)
brainLR.set_data_time_index(150)

stcHLR = mne.minimum_norm.apply_inverse(handLR, inv, lambda2, method, pick_ori=None)
brainLR = stcHLR.plot(subject=subject, surface='white', hemi='both', colormap='hot',
        smoothing_steps=5, transparent=True, subjects_dir=subjects_dir, time_viewer=False,
        clim=clim, figure=None)
brainLR.set_data_time_index(150)

# # read the data and write as fif
# raw = mne.io.bti.read_raw_bti(
#     'xc,hb,lf_c,rfhp0.1Hz', rename_channels=False, sort_by_ch_name=False)
# raw.pick_types(meg=True)
# raw.save('som-raw.fif')
# # filter
# raw = mne.io.read_raw_fif('som-raw.fif', preload=True,)
# raw.filter(1, 20)
# # make epochs and compute noise covariance
# events = mne.read_events('som-eve.fif')
# event_id = dict(handR=2,handL=4)
# epochs = mne.Epochs(raw, events, event_id, tmin=-0.1,
#                     tmax=0.3, baseline=(None, 0), preload=True)
# noise_cov = mne.compute_covariance(
#     epochs, tmax=0., method='empirical')
# mne.write_cov('BL-cov.fif',noise_cov)
# data_cov = mne.compute_covariance(epochs, method='empirical')
# mne.write_cov('all-cov.fif',data_cov)
#
# handR = epochs['handR'].average()
# handL = epochs['handL'].average()
# handLR=handL.copy()
# handLR.data=handL.data+handR.data
# # butterfly plot
# handLR.plot()
# # topography plot
# handLR.plot_topomap(times=(0.05))
# handL.save('handL-ave.fif')
# handR.save('handR-ave.fif')
# handLR.save('handLR-ave.fif')
