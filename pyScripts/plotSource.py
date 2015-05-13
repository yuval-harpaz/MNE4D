# for the figure to open well run this script
# in ipython, call it like this:   ipython --gui=wx

#taken from http://pysurfer.github.io/auto_examples/plot_meg_inverse_solution.html

import numpy as np
from surfer import Brain, TimeViewer
from surfer.io import read_stc


brain = Brain('fsaverage', 'both', 'pial', views='caudal')
stc = read_stc('fsaverage_wbw-meg-lh.stc')
data = stc['data']
vertices = stc['vertices']
time = 1e3 * np.linspace(stc['tmin'], stc['tmin'] + data.shape[1] * stc['tstep'], data.shape[1])
colormap = 'hot'
time_label = 'time=%0.2f ms'
brain.add_data(data, colormap=colormap, vertices=vertices, smoothing_steps=10,
               time=time, time_label=time_label, hemi='lh')

stc = read_stc('fsaverage_wbw-meg-rh.stc')
data = stc['data']
vertices = stc['vertices']
brain.add_data(data, colormap=colormap, vertices=vertices, smoothing_steps=10,
               time=time, time_label=time_label, hemi='rh')
#brain.set_data_time_index(2)
#brain.scale_data_colormap(fmin=13, fmid=18, fmax=22, transparent=True)
viewer = TimeViewer(brain)



