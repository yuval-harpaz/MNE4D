 # ipython --gui=wx
from os import chdir
from scipy.io import loadmat
from surfer import Brain
import numpy as np
from mne import read_forward_solution

chdir('/home/yuval/Data/marik/som2/MNE')
pow = loadmat('pow1.mat')
pow=pow['pow']
powL=np.empty(4098)
powR=powL
powL=pow[0,:4098]
powR=pow[0,4098:]
fwd=read_forward_solution('fixed1-fwd.fif')
vertL=fwd['src'][0]['vertno']
vertR=fwd['src'][1]['vertno']

brain = Brain('Marik', 'both', 'white', views='dorsal')
brain.add_data(powL, colormap='hot', vertices=vertL, smoothing_steps=5, hemi='lh')
brain.add_data(powR, colormap='hot', vertices=vertR, smoothing_steps=5, hemi='rh')
brain.scale_data_colormap(fmin=0, fmid=pow.max()/2, fmax=pow.max(), transparent=True)

