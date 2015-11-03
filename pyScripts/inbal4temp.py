import mne
from os import environ
from shutil import copyfile
import surfer


# this part is only necessary when running pycharm from louncher,
# and only for running watershed.# this part can be avoided when
# running pycharm from terminal or when running the script from
# ipython you opened in a terminal.
# not going through the terminal, you must set environment variables
# according to freesurfer setup.
subject = 'inbal4temp'
freesurfer_home = "/usr/local/freesurfer"
subjects_dir = freesurfer_home + "/subjects"
environ["FREESURFER_HOME"] = freesurfer_home
mne_bin = "/home/yuval/Programs/MNE-2.7.3-3268-Linux-x86_64/bin"
path = environ['PATH']
path = path + ":" + freesurfer_home + "/bin:" + mne_bin
environ['PATH'] = path
ld_lib = environ['LD_LIBRARY_PATH']
ld_lib = ld_lib + ":" + freesurfer_home + "/lib"
environ['LD_LIBRARY_PATH'] = ld_lib
#


# watershed - make BEM model with freesurfer
ws = mne.bem.make_watershed_bem(
    subject=subject, subjects_dir=subjects_dir, overwrite=True)
copyfile(subjects_dir + "/" + subject + "/bem/watershed/" + subject +
         "_inner_skull_surface", subjects_dir + "/" + subject + "/bem/inner_skull.surf")

cd ~/Data/inbal/4temp

# read the data and write as fif

raw = mne.io.bti.read_raw_bti(
    'rs,xc,hb,lf_c,rfhp0.1Hz', rename_channels=False, sort_by_ch_name=False)
raw.save('inbal4temp-raw.fif')


bem_model = mne.make_bem_model(
    subject=subject, subjects_dir=subjects_dir, conductivity=(0.3,))
bem_solution = mne.make_bem_solution(bem_model)
# /usr/local/freesurfer/subjects/aliceIdan/bem
mne.write_bem_solution(
    subjects_dir + "/" + subject + "/bem/" + subject + "-bem.fif", bem_solution)

# check BEM model
mne.viz.plot_bem(subject='aliceIdan',
                 subjects_dir='/usr/local/freesurfer/subjects', orientation='coronal')

# mark fiducials in the GUI, nudge and save
mne.gui.coregistration(
    subject=subject, subjects_dir=subjects_dir, inst='inbal4temp-raw.fif')


# filter
raw = mne.io.read_raw_fif('inbal4temp-raw.fif', preload=True,)
raw.pick_types('mag')
raw.filter(1, 40)
# make epochs and compute noise covariance
events = mne.read_events('4-eve.fif')
event_id = dict(beep=100)
epochs = mne.Epochs(raw, events, event_id, tmin=-
                    0.1, tmax=0.3, baseline=(None, 0), preload=True)
noise_cov = mne.compute_covariance(
    epochs, tmax=0., method=['shrunk', 'empirical'])
fig_cov, fig_spectra = mne.viz.plot_cov(noise_cov, raw.info)

aud = epochs['beep'].average()
# butterfly plot
aud.plot()
# topography plot
aud.plot_topomap(times=(0.092, 0.135, 0.2), ch_type='mag')

# make forward solution
src = mne.setup_source_space(
    subject, subjects_dir=subjects_dir, add_dist=False, overwrite=True)
trans = 'inbal4temp-trans.fif'
bem = subjects_dir + '/' + subject + '/bem/' + subject + '-bem.fif'

# Note that forward solutions can also be read with read_forward_solution
fwd = mne.make_forward_solution(
    raw.info, trans, src, bem, fname='inbal4temp-fwd.fif', meg=True, eeg=False, mindist=5.0, n_jobs=2, overwrite=True)

inv = mne.minimum_norm.make_inverse_operator(raw.info, fwd, noise_cov)
mne.minimum_norm.write_inverse_operator('inbal4temp-inv.fif', inv)
snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"
stc = mne.minimum_norm.apply_inverse(aud, inv, lambda2, method, pick_ori=None)


# plot the subject's brain with pysurfer
%gui
%gui wx
time = 0.092
tidx = abs(aud.times - time).argmin()
stcR = stc.rh_data[:, tidx]
stcL = stc.lh_data[:, tidx]
verticesR = stc.rh_vertno
verticesL = stc.lh_vertno
colormap = 'hot'
# export SUBJECTS_DIR=/usr/local/freesurfer/subjects/
brain = surfer.Brain(subject, 'both', 'white',
                     views='caudal', subjects_dir=subjects_dir)
brain.add_data(stcL, colormap=colormap,
               vertices=verticesL, smoothing_steps=10,  hemi='lh')
brain.add_data(stcR, colormap=colormap,
               vertices=verticesR, smoothing_steps=10, hemi='rh')
maxval = max(stcL.max(), stcR.max())
brain.scale_data_colormap(
    fmin=0, fmid=maxval / 2, fmax=maxval, transparent=True)

stc.plot(subject=subject, surface='pial', hemi='both', colormap='hot',
         smoothing_steps=10, transparent=True, subjects_dir=subjects_dir, time_viewer=True)

# now with the original brain
cd ../4/
subject = 'inbal4'
srcOrig = mne.setup_source_space(
    subject=subject, subjects_dir=subjects_dir, add_dist=False, overwrite=True)
transOrig = '4_raw-trans.fif'
bemOrig = subjects_dir + '/' + subject + \
    '/bem/' + subject + '-5120-bem-sol.fif'

# Note that forward solutions can also be read with read_forward_solution
fwdOrig = mne.make_forward_solution(
    raw.info, transOrig, srcOrig, bemOrig, meg=True, eeg=False, mindist=5.0, n_jobs=2, overwrite=True)

invOrig = mne.minimum_norm.make_inverse_operator(raw.info, fwdOrig, noise_cov)
# mne.minimum_norm.write_inverse_operator('inbal4temp-inv.fif',inv)
snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"
stcOrig = mne.minimum_norm.apply_inverse(
    aud, invOrig, lambda2, method, pick_ori=None)
time = 0.092
tidx = abs(aud.times - time).argmin()
stcR = stcOrig.rh_data[:, tidx]
stcL = stcOrig.lh_data[:, tidx]
verticesR = stcOrig.rh_vertno
verticesL = stcOrig.lh_vertno
colormap = 'hot'
# export SUBJECTS_DIR=/usr/local/freesurfer/subjects/
brainO = surfer.Brain(
    subject, 'both', 'white', views='caudal', subjects_dir=subjects_dir)
brainO.add_data(stcL, colormap=colormap,
                vertices=verticesL, smoothing_steps=10,  hemi='lh')
brainO.add_data(stcR, colormap=colormap,
                vertices=verticesR, smoothing_steps=10, hemi='rh')
maxval = max(stcL.max(), stcR.max())
brainO.scale_data_colormap(
    fmin=0, fmid=maxval / 2, fmax=maxval, transparent=True)

stcOrig.plot(subject=subject, surface='pial', hemi='both', colormap='hot',
             smoothing_steps=10, transparent=True, subjects_dir=subjects_dir, time_viewer=True)
