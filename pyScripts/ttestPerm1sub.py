from os import chdir
import os.path
from termcolor import colored
#from surfer.io import read_stc
from mne import read_source_estimate
import numpy as np
from scipy import stats as stats
from mne.stats import spatio_temporal_cluster_test, summarize_clusters_stc
from mne import spatial_tris_connectivity, grade_to_tris
#subjects = ['idan', 'inbal', 'liron', 'maor', 'mark', 'ohad', 'odelia', 'yoni'];
sub='idan'
#fsSub='alice'+sub[0].upper()+sub[1:]
chdir('/home/yuval/Copy/MEGdata/alice/'+sub+'/MNE')
stc = read_source_estimate('mne_dSPM_fsa')

stc.resample(50) #50Hz new sampling rate
n_vertices_fsave, n_times = stc.data.shape
tstep = stc.tstep

n_subjects1, n_subjects2 = 7, 9
print('Simulating data for %d and %d subjects.' % (n_subjects1, n_subjects2))

#    Let's make sure our results replicate, so set the seed.
np.random.seed(0)
X1 = np.random.randn(n_vertices_fsave, n_times, n_subjects1) * 10
X2 = np.random.randn(n_vertices_fsave, n_times, n_subjects2) * 10
X1[:, :, :] += stc.data[:, :, np.newaxis]
# make the activity bigger for the second set of subjects
X2[:, :, :] += 3 * stc.data[:, :, np.newaxis]

#    We want to compare the overall activity levels for each subject
X1 = np.abs(X1)  # only magnitude
X2 = np.abs(X2)  # only magnitude

###############################################################################
# Compute statistic

#    To use an algorithm optimized for spatio-temporal clustering, we
#    just pass the spatial connectivity matrix (instead of spatio-temporal)
print('Computing connectivity.')
connectivity = spatial_tris_connectivity(grade_to_tris(5))

#    Note that X needs to be a list of multi-dimensional array of shape
#    samples (subjects_k) x time x space, so we permute dimensions
X1 = np.transpose(X1, [2, 1, 0])
X2 = np.transpose(X2, [2, 1, 0])
X = [X1, X2]

#    Now let's actually do the clustering. This can take a long time...
#    Here we set the threshold quite high to reduce computation.
p_threshold = 0.0001
f_threshold = stats.distributions.f.ppf(1. - p_threshold / 2., n_subjects1 - 1, n_subjects2 - 1)
print('Clustering.')
T_obs, clusters, cluster_p_values, H0 = clu = spatio_temporal_cluster_test(X, connectivity=connectivity, n_jobs=2, threshold=f_threshold)
#    Now select the clusters that are sig. at p < 0.05 (note that this value
#    is multiple-comparisons corrected).
good_cluster_inds = np.where(cluster_p_values < 0.05)[0]

###############################################################################
# Visualize the clusters

print('Visualizing clusters.')

#    Now let's build a convenient representation of each cluster, where each
#    cluster becomes a "time point" in the SourceEstimate
fsave_vertices = [np.arange(10242), np.arange(10242)]
stc_all_cluster_vis = summarize_clusters_stc(clu, tstep=tstep,
                                             vertno=fsave_vertices,
                                             subject='fsaverage')

#    Let's actually plot the first "time point" in the SourceEstimate, which
#    shows all the clusters, weighted by duration
subjects_dir = op.join(data_path, 'subjects')
# blue blobs are for condition A != condition B
brain = stc_all_cluster_vis.plot('fsaverage', 'inflated', 'both',
                                 subjects_dir=subjects_dir,
                                 time_label='Duration significant (ms)',
                                 fmin=0, fmid=25, fmax=50)
brain.set_data_time_index(0)
brain.scale_data_colormap(fmin=0, fmid=25, fmax=50, transparent=True)
brain.show_view('lateral')
brain.save_image('clusters.png')