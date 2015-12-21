import mne
import surfer
import numpy as np
from compute_g2 import g2
#cd ~/Data/epilepsy/b391/3


# rawEmpty = mne.io.bti.read_raw_bti('/home/yuval/Data/emptyRoom/lf_c,rfhp0.1Hz', rename_channels=False, sort_by_ch_name=False)
# rawEmpty.pick_types('mag')
# rawEmpty.filter(20,70)


empty_cov = mne.read_cov('/home/yuval/Data/emptyRoom/epi20_70-cov.fif')

subject = 'b391'
freesurfer_home = "/usr/local/freesurfer"
subjects_dir = freesurfer_home + "/subjects"

raw=mne.io.Raw('0-raw.fif', preload=True)
raw.pick_types('mag')
raw.filter(20,70)
data_cov = mne.compute_raw_covariance(raw)
src = mne.setup_source_space(
    subject, subjects_dir=subjects_dir, add_dist=False, fname=None)
bem = subjects_dir + '/' + subject + '/bem/' + subject + '-bem.fif'
trans = 'b391-trans.fif'

fwd = mne.read_forward_solution('3-fwd.fif')
fwd1 = mne.convert_forward_solution(fwd, surf_ori=True)
fwd2 = mne.convert_forward_solution(fwd, surf_ori=True, force_fixed=True)
#mne.minimum_norm.write_inverse_operator('3_LCMV-inv.fif', inv)


dur=np.int(round(2034.5/4)+1)

# snr = 3.0
# lambda2 = 1.0 / snr ** 2
samps=np.arange(0,raw._data.shape[1],dur)
samps=samps[0:-1]
Kur=np.zeros((fwd['nsource']))
for sampi in range(0,len(samps)):
    start=samps[sampi]
    stop=start+dur
    stc = mne.beamformer.lcmv_raw(raw, fwd2, empty_cov, data_cov,start=start, stop=stop)
    kur=g2(stc.data)
    kur[kur<0]=0
    Kur=Kur+kur
    print("DONE "+str(sampi+1)+" of "+str(len(samps)))


Kur=Kur/sampi
np.save('KurLCMVfixed',Kur)
verticesL = stc.lh_vertno
verticesR = stc.rh_vertno
stcL=Kur[0:len(verticesL)]
stcR=Kur[len(verticesL):len(Kur)]
colormap = 'hot'

brain = surfer.Brain(subject, 'both', 'pial',
                     views='lateral', subjects_dir=subjects_dir)
brain.add_data(stcL, colormap=colormap,
               vertices=verticesL, smoothing_steps=10,  hemi='lh')
brain.add_data(stcR, colormap=colormap,
               vertices=verticesR, smoothing_steps=10, hemi='rh')
maxval = max(stcL.max(), stcR.max())
brain.scale_data_colormap(
    fmin=maxval/3, fmid=2*maxval / 3, fmax=maxval, transparent=True)

brain = surfer.Brain(subject, 'both', 'white',
                     views='lateral', subjects_dir=subjects_dir)
brain.add_data(stcL, colormap=colormap,
               vertices=verticesL, smoothing_steps=10,  hemi='lh')
brain.add_data(stcR, colormap=colormap,
               vertices=verticesR, smoothing_steps=10, hemi='rh')
maxval = max(stcL.max(), stcR.max())
brain.scale_data_colormap(
    fmin=maxval * 0.4, fmid=maxval * 0.6, fmax=maxval * 0.8, transparent=True)


# load VS with scipy.io.loadmat
verticesL=np.load('verticesL.npy')
verticesR=np.load('verticesR.npy')
stcL=VS[0,0:len(verticesL)]
stcR=VS[0,len(verticesL):len(VS.T)]
colormap = 'hot'

brain = surfer.Brain(subject, 'both', 'pial',
                     views='lateral', subjects_dir=subjects_dir)
brain.add_data(stcL, colormap=colormap,
               vertices=verticesL, smoothing_steps=10,  hemi='lh')
brain.add_data(stcR, colormap=colormap,
               vertices=verticesR, smoothing_steps=10, hemi='rh')
maxval = max(stcL.max(), stcR.max())
brain.scale_data_colormap(
    fmin=maxval/3, fmid=2*maxval / 3, fmax=maxval, transparent=True)

brain.scale_data_colormap(
    fmin=maxval * 0.4, fmid=maxval * 0.6, fmax=maxval * 0.8, transparent=True)