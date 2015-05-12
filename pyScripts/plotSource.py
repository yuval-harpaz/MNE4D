# for the figure to open well run this script
# in ipython, call it like this:   ipython --gui=wx
from mne.datasets import sample
from mne.minimum_norm import read_inverse_operator
fname='ohad_raw-oct-6-meg-inv.fif'
inv = read_inverse_operator(fname)
print("Method: %s" % inv['methods'])
print("fMRI prior: %s" % inv['fmri_prior'])
print("Number of sources: %s" % inv['nsource'])
print("Number of channels: %s" % inv['nchan'])
lh_points = inv['src'][0]['rr']
lh_faces = inv['src'][0]['use_tris']
rh_points = inv['src'][1]['rr']
rh_faces = inv['src'][1]['use_tris']
from mayavi import mlab
mlab.figure(size=(600, 600), bgcolor=(0, 0, 0))
mlab.triangular_mesh(lh_points[:, 0], lh_points[:, 1], lh_points[:, 2],
                     lh_faces)
mlab.triangular_mesh(rh_points[:, 0], rh_points[:, 1], rh_points[:, 2],
                     rh_faces)

