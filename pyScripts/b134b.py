import mne
from os import environ
from shutil import copyfile
import surfer

# open pycharm using a terminal

subject = 'b134b'
# environ["subject"] = subject
freesurfer_home = "/usr/local/freesurfer"
subjects_dir = freesurfer_home + "/subjects"
# environ["FREESURFER_HOME"] = freesurfer_home
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
# copy file
freesurfer_home = "/usr/local/freesurfer"
subjects_dir = freesurfer_home + "/subjects"
copyfile(subjects_dir + "/" + subject + "/bem/watershed/" + subject +
         "_inner_skull_surface", subjects_dir + "/" + subject + "/bem/inner_skull.surf")




bem_model = mne.make_bem_model(
    subject=subject, subjects_dir=subjects_dir, conductivity=(0.3,))
bem_solution = mne.make_bem_solution(bem_model)
# /usr/local/freesurfer/subjects/aliceIdan/bem
mne.write_bem_solution(
    subjects_dir + "/" + subject + "/bem/" + subject + "-bem.fif", bem_solution)

# check BEM model
mne.viz.plot_bem(subject=subject,
                 subjects_dir=subjects_dir, orientation='coronal')

# read the data and write as fif
cd ~/Data/epilepsy/b134b/2
raw = mne.io.bti.read_raw_bti(
    'hb,lf_c,rfhp1.0Hz', rename_channels=False, sort_by_ch_name=False)
raw.save('hb,lf-raw.fif')

# mark fiducials in the GUI, nudge and save
mne.gui.coregistration(
    subject=subject, subjects_dir=subjects_dir, inst='hb,lf-raw.fif')


# filter
raw = mne.io.read_raw_fif('hb,lf-raw.fif')
# raw.pick_types('mag')
# make epochs and compute noise covariance
events = mne.read_events('epi-eve.fif')
# event_id = dict(quiet=1,rythm=2,hf=3)
event_id = dict(quiet=1)
epochsBL = mne.Epochs(raw, events, event_id,
                    tmin=0, tmax=0.5, baseline=(None, None), preload=True)
BL_cov = mne.compute_covariance(epochsBL, tmax=0.5, method='empirical')
BL_cov.save('empirical_BL-cov.fif')
fig_cov, fig_spectra = mne.viz.plot_cov(BL_cov, raw.info)

# make forward solution
src = mne.setup_source_space(
    subject, subjects_dir=subjects_dir, add_dist=False, overwrite=True)
trans = 'b134-trans.fif'
bem = subjects_dir + '/' + subject + '/bem/' + subject + '-bem.fif'

# Note that forward solutions can also be read with read_forward_solution
fwd = mne.make_forward_solution(
    raw.info, trans, src, bem, fname='b134-fwd.fif', meg=True, eeg=False, mindist=5.0, n_jobs=4, overwrite=True)
fwd = mne.convert_forward_solution(fwd, surf_ori=True)
invBL = mne.minimum_norm.make_inverse_operator(raw.info, fwd, BL_cov, fixed=True)
mne.minimum_norm.write_inverse_operator('BL-inv.fif', invBL)

# EPMTY ROOM
rawEmpty = mne.io.bti.read_raw_bti('/home/yuval/Data/emptyRoom/lf_c,rfhp0.1Hz', rename_channels=False, sort_by_ch_name=False)
rawEmpty.pick_types('mag')
rawEmpty.filter(1,None)
raw.save('/home/yuval/Data/emptyRoom/lf,1hp_raw.fif',overwrite='True')
events = mne.read_events('/home/yuval/Data/emptyRoom/1s-eve.fif')
# event_id = dict(quiet=1,rythm=2,hf=3)
event_id = dict(empty=1)
epochsEmpty = mne.Epochs(raw, events, event_id,
                    tmin=0, tmax=0.5, baseline=(None, None), preload=True)
empty_cov = mne.compute_covariance(epochsBL, method='empirical')
empty_cov.save('/home/yuval/Data/emptyRoom/empirical_hp1_0.5s-cov.fif')
# empty_cov=mne.read_cov('/home/yuval/Data/emptyRoom/empirical_hp1_0.5s-cov.fif')
invEmpty = mne.minimum_norm.make_inverse_operator(raw.info, fwd, empty_cov, fixed=True)
mne.minimum_norm.write_inverse_operator('Empty-inv.fif', invEmpty)

