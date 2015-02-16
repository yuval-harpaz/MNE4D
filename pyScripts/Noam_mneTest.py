__author__ = 'noam'

import mne
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

from mne.viz import plot_topo
from mne.minimum_norm import (make_inverse_operator, apply_inverse,
    write_inverse_operator, read_inverse_operator)
from mne.source_estimate import read_source_estimate
from mne.commands import mne_bti2fiff

import os.path as op
import numpy as np
from numpy.random import randn
from scipy import stats as stats

import mne
from mne import (io, spatial_tris_connectivity, compute_morph_matrix,
                 grade_to_tris)
from mne.epochs import equalize_epoch_counts
from mne.stats import (spatio_temporal_cluster_1samp_test,
                       summarize_clusters_stc)
from mne.viz import mne_analyze_colormap


try:
    from mne.time_frequency import induced_power
except:
    print('no induced_power module')

def getFileName(fname):
    return os.path.join(SUBJECT_FOLDER, '{}-{}.fif'.format(SUBJECT, fname))

SUBJECTS_DIR = '/home/noam/Documents/MEGdata/centipede/mne'
SUBJECT = 'Idan'
SUBJECT_FOLDER = os.path.join(SUBJECTS_DIR, SUBJECT)
RAW_4D = os.path.join(SUBJECT_FOLDER, 'rs,hb,lf_c,rfhp0.1Hz')
RAW = getFileName('raw')
EVO = getFileName('ave')
COV = getFileName('cov')
EPO = getFileName('epo')
FWD = getFileName('fwd')
INV = getFileName('inv')
# This file was created using
# mne_watershed_bem --atlas
# mne_setup_mri --overwrite
# Then, open mne_analyze and follow these instructions:
# http://martinos.org/mne/stable/manual/sampledata.html#chdijbig
MRI = os.path.join(SUBJECT_FOLDER, 'mri', 'transforms', 'Idan-trans.fif')
# The following files were created using created using:
# mne_watershed_bem --atlas --overwrite
# Them, copy the surface files from bem/watershed, and rename them
# like outer_skull_surface -> outer_skull.surf
# Then setup the forward model
# mne_setup_forward_model --homog --surf --ico 4 --overwrite
SRC = os.path.join(SUBJECT_FOLDER, 'bem', 'Idan-src.fif')
BEM = os.path.join(SUBJECT_FOLDER, 'bem', 'Idan-5120-bem-sol.fif')
# Source estimate
STC = os.path.join(SUBJECT_FOLDER, 'mne_dSPM_inverse_MEG')

def convertToFIF():
    sys.argv = ['', '-p', RAW_4D, '-o', RAW]
    mne_bti2fiff.run()


def loadRaw():
    # read the data
    raw = mne.io.Raw(RAW, preload=True)
    print(raw)
    return raw


def filter(raw):
    raw.filter(l_freq=1.0, h_freq=50.0)
    raw.save(RAW, overwrite=True)


def calcNoiseCov(raw=None):
    if (raw is None):
        raw = mne.io.Raw(RAW, preload=True)
    picks = mne.pick_types(raw.info, meg=True)
    events = mne.find_events(raw, stim_channel='STI 014')
    epoches = []
    for tmin, tmax in zip(np.arange(0, 3.5, 0.5), np.arange(0.5, 4, 0.5)):
        print((tmin, tmax))
        epoches.append(findEpoches(raw, picks, events, dict(onset=20), tmin=tmin, tmax=tmax, baseline=(None, None)))

    noiseCov = mne.compute_covariance([epo['onset'] for epo in epoches], tmax=None)
    # regularize noise covariance
    # noiseCov = mne.cov.regularize(noiseCov, evoked.info,
    #     mag=0.05, proj=True) # grad=0.05, eeg=0.1
    noiseCov.save(COV)
    allEpoches = findEpoches(raw, picks, events, dict(onset=20), tmin=0, tmax=3.5)
    evoked = allEpoches['onset'].average()
    evoked.save(EVO)


def calcEvoked(raw):
    picks = mne.pick_types(raw.info, meg=True)
    events = mne.find_events(raw, stim_channel='STI 014')
    print(events)
    epochs = findEpoches(raw, picks, events, dict(stay=60, leave=40), tmin=-3.0, tmax=0)
    # compute evoked response and noise covariance,and plot evoked
    epochs.save(EPO)
    evokedStay = epochs['stay'].average()
    evokedLeave = epochs['leave'].average()
    contrast = evokedStay - evokedLeave
    covStay = mne.compute_covariance(epochs['stay'], tmax=0)
    covLeave = mne.compute_covariance(epochs['leave'], tmax=0)
    covStay.save(getFileName('stay-cov'))
    covLeave.save(getFileName('leave-cov'))
    # evokedStay.plot()
    # evokedLeave.plot()
    # contrast.plot()

def plotEvokedDiff():
    epochs = loadEpoches()
    evokeds = [epochs[name].average() for name in 'stay', 'leave']
    colors = 'yellow', 'green'
    title = 'Stay vs Leave'
    plot_topo(evokeds, color=colors, title=title)

    conditions = [e.comment for e in evokeds]
    for cond, col, pos in zip(conditions, colors, (0.025, 0.07)):
        plt.figtext(0.775, pos, cond, color=col, fontsize=12)

    plt.show()

def calcInducedPower(raw):
    n_cycles = 2  # number of cycles in Morlet wavelet
    frequencies = np.arange(1, 50, 1)  # frequencies of interest
    Fs = raw.info['sfreq']  # sampling in Hz
    epoches = loadEpoches()
    epochesStay = getEpochesData('stay')
    power, phase_lock = induced_power(epochesStay, Fs=Fs, frequencies=frequencies, n_cycles=2, n_jobs=1)


def plotLeadField(fwd=None):
    if (fwd is None):
        fwd = mne.read_forward_solution(FWD)
    leadfield = fwd['sol']['data']
    print("Leadfield size : %d x %d" % leadfield.shape)
    magMap = mne.sensitivity_map(fwd, ch_type='mag', mode='fixed')
    picks = mne.pick_types(fwd['info'], meg=True, eeg=False)

    fig, ax = plt.subplots(1, 1, figsize=(10, 8), sharex=True)
    fig.suptitle('Lead field matrix (500 dipoles only)', fontsize=14)
    im = ax.imshow(leadfield[picks, :500], origin='lower', aspect='auto')
    ax.set_title('MEG')
    ax.set_xlabel('sources')
    ax.set_ylabel('sensors')
    plt.colorbar(im, ax=ax, cmap='RdBu_r')
    plt.show()

    plotOrientationSensitivity(magMap)
    plotMagSensitivity(magMap)


def plotOrientationSensitivity(magMap=None):
    if (magMap is None):
        fwd = mne.read_forward_solution(FWD)
        magMap = mne.sensitivity_map(fwd, ch_type='mag', mode='fixed')
    plt.figure()
    plt.hist(magMap.data.ravel(),
             bins=20, label='Magnetometers')
    plt.legend()
    plt.title('Normal orientation sensitivity')
    plt.xlabel('sensitivity')
    plt.ylabel('count')
    plt.show()


def plotMagSensitivity(magMap=None):
    if (magMap is None):
        fwd = mne.read_forward_solution(FWD)
        magMap = mne.sensitivity_map(fwd, ch_type='mag', mode='fixed')
    args = dict(fmin=0.1, fmid=0.5, fmax=0.9, smoothing_steps=7)
    magMap.plot(subject=SUBJECT, time_label='Sensitivity',
                  subjects_dir=SUBJECTS_DIR, **args)

def findEpoches(raw, picks,  events, event_id, tmin, tmax, baseline=(None, 0)):
    return mne.Epochs(raw=raw, events=events, event_id=event_id, tmin=tmin, tmax=tmax, proj=True,
        picks=picks, baseline=baseline, preload=True, reject=None) # reject can be dict(mag=4e-12)


def makeForwardSolution(n_jobs=1, usingEEG=False, outputFileName='fwd'):
    fwd = mne.make_forward_solution(RAW, mri=MRI, src=SRC, bem=BEM,
        fname=FWD, meg=True, eeg=usingEEG, mindist=5.0,
        n_jobs=n_jobs, overwrite=True)
    # convert to surface orientation for better visualization
    fwd = mne.convert_forward_solution(fwd, surf_ori=True)
    return fwd


def makeInverseOperator():
    # http://martinos.org/mne/stable/auto_examples/inverse/plot_make_inverse_operator.html
    snr = 3.0
    lambda2 = 1.0 / snr ** 2

    # Load data
    evoked = mne.read_evokeds(EVO, condition=0, baseline=(None, 0))
    forward_meg = mne.read_forward_solution(FWD, surf_ori=True)
    noise_cov = mne.read_cov(COV)

    # regularize noise covariance
    noise_cov = mne.cov.regularize(noise_cov, evoked.info,
        mag=0.05, proj=True) # grad=0.05, eeg=0.1

    # Restrict forward solution as necessary for MEG
    forward_meg = mne.pick_types_forward(forward_meg, meg=True, eeg=False)

    # make an M/EEG, MEG-only, and EEG-only inverse operators
    info = evoked.info
    inverse_operator_meg = make_inverse_operator(info, forward_meg, noise_cov,
        loose=0.2, depth=0.8)

    write_inverse_operator(INV, inverse_operator_meg)

    # Compute inverse solution
    stcs_meg = apply_inverse(evoked, inverse_operator_meg, lambda2, "dSPM",
        pick_ori=None)

    # Save result in stc files
    stcs_meg.save(STC)
    plotActivationTS(stcs_meg)


def plotActivationTS(stcs_meg):
    plt.close('all')
    plt.figure(figsize=(8, 6))
    name = 'MEG'
    stc = stcs_meg
    plt.plot(1e3 * stc.times, stc.data[::150, :].T)
    plt.ylabel('%s\ndSPM value' % str.upper(name))
    plt.xlabel('time (ms)')
    plt.show()


def plot3DActivity(stc=None):
    if (stc is None):
        stc = read_source_estimate(STC)
    # Plot brain in 3D with PySurfer if available. Note that the subject name
    # is already known by the SourceEstimate stc object.
    brain = stc.plot(surface='inflated', hemi='rh', subjects_dir=SUBJECTS_DIR, subject=SUBJECT)
    brain.scale_data_colormap(fmin=8, fmid=12, fmax=15, transparent=True)
    brain.show_view('lateral')

    # use peak getter to move vizualization to the time point of the peak
    vertno_max, time_idx = stc.get_peak(hemi='rh', time_as_index=True)

    brain.set_data_time_index(time_idx)

    # draw marker at maximum peaking vertex
    brain.add_foci(vertno_max, coords_as_verts=True, hemi='rh', color='blue',
                   scale_factor=0.6)
    brain.save_image(getPngName('dSPM_map'))


def permuationTest():
    # http://martinos.org/mne/stable/auto_examples/stats/plot_cluster_stats_spatio_temporal.html#example-stats-plot-cluster-stats-spatio-temporal-py
    epoches = loadEpoches()
    epo1 = epoches['stay']
    epo2 = epoches['leave']
    #    Equalize trial counts to eliminate bias (which would otherwise be
    #    introduced by the abs() performed below)
    equalize_epoch_counts([epo1, epo2])

    ###############################################################################
    # Transform to source space
    snr = 3.0
    lambda2 = 1.0 / snr ** 2
    method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)
    inverse_operator = read_inverse_operator(INV)
    sample_vertices = [s['vertno'] for s in inverse_operator['src']]

    #    Let's average and compute inverse, resampling to speed things up
    evoked1 = epo1.average()
    evoked1.resample(50)
    condition1 = apply_inverse(evoked1, inverse_operator, lambda2, method)
    evoked2 = epo2.average()
    evoked2.resample(50)
    condition2 = apply_inverse(evoked2, inverse_operator, lambda2, method)

    #    Let's only deal with t > 0, cropping to reduce multiple comparisons
    # condition1.crop(0, None)
    # condition2.crop(0, None)
    tmin = condition1.tmin
    tstep = condition1.tstep

    ###############################################################################
    # Transform to common cortical space

    #    Normally you would read in estimates across several subjects and morph
    #    them to the same cortical space (e.g. fsaverage). For example purposes,
    #    we will simulate this by just having each "subject" have the same
    #    response (just noisy in source space) here. Note that for 7 subjects
    #    with a two-sided statistical test, the minimum significance under a
    #    permutation test is only p = 1/(2 ** 6) = 0.015, which is large.
    n_vertices_sample, n_times = condition1.data.shape
    n_subjects = 7
    print('Simulating data for %d subjects.' % n_subjects)

    #    Let's make sure our results replicate, so set the seed.
    np.random.seed(0)
    X = randn(n_vertices_sample, n_times, n_subjects, 2) * 10
    X[:, :, :, 0] += condition1.data[:, :, np.newaxis]
    X[:, :, :, 1] += condition2.data[:, :, np.newaxis]

    #    It's a good idea to spatially smooth the data, and for visualization
    #    purposes, let's morph these to fsaverage, which is a grade 5 source space
    #    with vertices 0:10242 for each hemisphere. Usually you'd have to morph
    #    each subject's data separately (and you might want to use morph_data
    #    instead), but here since all estimates are on 'sample' we can use one
    #    morph matrix for all the heavy lifting.
    fsave_vertices = [np.arange(10242), np.arange(10242)]
    morph_mat = compute_morph_matrix('Idan', 'fsaverage', sample_vertices,
                                     fsave_vertices, 20, SUBJECTS_DIR, )
    n_vertices_fsave = morph_mat.shape[0]

    #    We have to change the shape for the dot() to work properly
    X = X.reshape(n_vertices_sample, n_times * n_subjects * 2)
    print('Morphing data.')
    X = morph_mat.dot(X)  # morph_mat is a sparse matrix
    X = X.reshape(n_vertices_fsave, n_times, n_subjects, 2)

    #    Finally, we want to compare the overall activity levels in each condition,
    #    the diff is taken along the last axis (condition). The negative sign makes
    #    it so condition1 > condition2 shows up as "red blobs" (instead of blue).
    X = np.abs(X)  # only magnitude
    X = X[:, :, :, 0] - X[:, :, :, 1]  # make paired contrast


    ###############################################################################
    # Compute statistic

    #    To use an algorithm optimized for spatio-temporal clustering, we
    #    just pass the spatial connectivity matrix (instead of spatio-temporal)
    print('Computing connectivity.')
    connectivity = spatial_tris_connectivity(grade_to_tris(5))

    #    Note that X needs to be a multi-dimensional array of shape
    #    samples (subjects) x time x space, so we permute dimensions
    X = np.transpose(X, [2, 1, 0])

    #    Now let's actually do the clustering. This can take a long time...
    #    Here we set the threshold quite high to reduce computation.
    p_threshold = 0.001
    t_threshold = -stats.distributions.t.ppf(p_threshold / 2., n_subjects - 1)
    print('Clustering.')
    T_obs, clusters, cluster_p_values, H0 = clu = \
        spatio_temporal_cluster_1samp_test(X, connectivity=connectivity, n_jobs=2,
                                           threshold=t_threshold)
    #    Now select the clusters that are sig. at p < 0.05 (note that this value
    #    is multiple-comparisons corrected).
    good_cluster_inds = np.where(cluster_p_values < 0.05)[0]

    ###############################################################################
    # Visualize the clusters

    print('Visualizing clusters.')

    #    Now let's build a convenient representation of each cluster, where each
    #    cluster becomes a "time point" in the SourceEstimate
    stc_all_cluster_vis = summarize_clusters_stc(clu, tstep=tstep,
                                                 vertno=fsave_vertices,
                                                 subject='fsaverage')

    #    Let's actually plot the first "time point" in the SourceEstimate, which
    #    shows all the clusters, weighted by duration
    colormap = mne_analyze_colormap(limits=[0, 10, 50])
    # blue blobs are for condition A < condition B, red for A > B
    brain = stc_all_cluster_vis.plot('fsaverage', 'inflated', 'both', colormap,
                                     subjects_dir=SUBJECTS_DIR,
                                     time_label='Duration significant (ms)')
    brain.set_data_time_index(0)
    # The colormap requires brain data to be scaled -fmax -> fmax
    brain.scale_data_colormap(fmin=-50, fmid=0, fmax=50, transparent=False)
    brain.show_view('lateral')
    brain.save_image('clusters.png')


def loadEpoches(epochesName='epo'):
    return mne.read_epochs(getFileName(epochesName))


def loadEvoked(evokedName, condition):
    return mne.read_evokeds(getFileName(evokedName), condition=condition, baseline=(None, 0), proj=True)


def getEpochesData(epochs, condName):
    return epochs[condName].get_data()


def readInverseOp(invOpFileName):
    inverse_operator = read_inverse_operator(invOpFileName)
    return inverse_operator

def getPngName(fname):
    return os.path.join(SUBJECT_FOLDER, '{}.png'.format(fname))

if __name__ == '__main__':
    # raw = loadRaw()
    # filter(raw)
    # calcNoiseCov()
    # plotEvokedDiff()
    # epoches = loadEpoches()
    # makeForwardSolution(n_jobs=4)
    # plotLeadField()
    # plotMagSensitivity()
    # makeInverseOperator()
    # plot3DActivity()
    permuationTest()
    print('finish!')