from os import chdir
from scipy.io import loadmat
from surfer import Brain
import numpy as np
from mne import read_forward_solution

chdir('/home/yuval/Data/marik/som2/MNE')
fwd=read_forward_solution('fixed1-fwd.fif')
chdir('/home/yuval/Data/marik/som2/1')
pow = loadmat('src.mat')
powL=pow['srcMultL']

brain = Brain('Marik', 'both', 'white', views='dorsal', subjects_dir='/usr/local/freesurfer/subjects')
%gui wx

brain.add_data(powL, colormap='hot', smoothing_steps=1, hemi='lh')
brain.scale_data_colormap(fmin=0, fmid=powL.max()/2, fmax=powL.max(), transparent=True)

powL=pow['srcL']
brain = Brain('Marik', 'both', 'white', views='dorsal', subjects_dir='/usr/local/freesurfer/subjects')
brain.add_data(powL, smoothing_steps=1, hemi='lh',colormap='hot', colorbar=False,time_label=None)
brain.scale_data_colormap(fmin=0, fmid=powL.max()/2, fmax=powL.max(), transparent=True)