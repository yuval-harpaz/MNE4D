__author__ = 'yuval'


import mne
from os import chdir
#from IPython.display import Image
#from mayavi import mlab
# mne_bti2fiff.py -p xc,hb,lf,9_34c,rfhp0.1Hz -o idan_raw.fif
chdir("/home/yuval/wsMNE/")
raw=mne.io.bti.read_raw_bti('xc,hb,lf_c,rfDC')
raw.save('idanTest-raw.fif')
raw=mne.io.Raw('idanTest-raw.fif')

subjects_dir='/usr/local/freesurfer/subjects'
mne.viz.plot_bem(subject='aliceIdan',subjects_dir='/usr/local/freesurfer/subjects', orientation='coronal')


raw=mne.io.read_raw_fif('idan_raw.fif')
info = raw.info

mne.gui.coregistration()

mri="/home/yuval/Copy/MEGdata/alice/idan/MNE/idan_raw-trans.fif"

fig = mne.viz.plot_trans(info, mri, subject='aliceIdan', dig=False, subjects_dir=subjects_dir);
mlab.savefig('coreg.jpg')
# Image(filename='coreg.jpg', width=500)

bem_model = mne.make_bem_model(subject='aliceIdan', subjects_dir=subjects_dir, conductivity=(0.3,))
bem_solution = mne.make_bem_solution(bem_model)
# /usr/local/freesurfer/subjects/aliceIdan/bem
mne.write_bem_solution('/usr/local/freesurfer/subjects/aliceIdan/bem/aliceIdan-bem.fif',bem_solution)

src_fsaverage = mne.setup_source_space('fsaverage', spacing='oct6', subjects_dir=subjects_dir, add_dist=False, overwrite=True)
src_sub = mne.morph_source_spaces(src_fsaverage, 'aliceIdan', subjects_dir=subjects_dir)
#
