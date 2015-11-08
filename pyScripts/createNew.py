import mne

# copy fsaverage to a new subjects_dir
mne_root = "/home/yuval/Programs/MNE-2.7.3-3268-Linux-x86_64"
freesurfer_home = "/usr/local/freesurfer"
subjects_dir='/home/yuval/Data/subjects/'
mne.create_default_subject(mne_root=mne_root,fs_home=freesurfer_home,subjects_dir=subjects_dir)

# corregistration
subject = 'fsaverage'
mne.gui.coregistration(
    subject=subject, subjects_dir=subjects_dir, inst='/home/yuval/Data/inbal/4/4_raw.fif')

