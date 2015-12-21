import mne
import surfer
import numpy as np
from compute_g2 import g2
#cd ~/Data/epilepsy/b391/3


subject = 'b391'
freesurfer_home = "/usr/local/freesurfer"
subjects_dir = freesurfer_home + "/subjects"
sphere = (0, 0, 0, 120)
mri = subjects_dir + '/' + subject + '/mri/aseg.mgz'
bem = subjects_dir + '/' + subject + '/bem/' + subject + '-bem.fif'
src2 = mne.setup_volume_source_space(subject=subject, sphere=sphere, subjects_dir=subjects_dir, bem=bem, mri=mri)
trans = 'b391-trans.fif'
mne.do_forward_solution(subject, mri=mri, src=src2,bem=bem, trans=trans)
raw=mne.io.Raw('0-raw.fif')
fwd = mne.make_forward_solution(
     raw.info, trans, src2, bem, fname='b391vol-fwd.fif', meg=True, eeg=False, mindist=5.0, n_jobs=4, overwrite=True)
# lh_cereb = setup_volume_source_space(subj, mri=aseg_fname, sphere=sphere,
#                                      volume_label=volume_label,
#                                      subjects_dir=subjects_dir)




# rawEmpty = mne.io.bti.read_raw_bti('/home/yuval/Data/emptyRoom/lf_c,rfhp0.1Hz', rename_channels=False, sort_by_ch_name=False)
# rawEmpty.pick_types('mag')
# rawEmpty.filter(20,70)


empty_cov = mne.read_cov('/home/yuval/Data/emptyRoom/epi20_70-cov.fif')


raw=mne.io.Raw('0-raw.fif', preload=True)
raw.pick_types('mag')
raw.filter(20,70)
data_cov = mne.compute_raw_covariance(raw)

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
    stc = mne.beamformer.lcmv_raw(raw, fwd, empty_cov, data_cov,start=start, stop=stop)
    kur=g2(stc.data)
    kur[kur<0]=0
    Kur=Kur+kur
    print("DONE "+str(sampi+1)+" of "+str(len(samps)))


Kur=Kur/sampi
# np.save('KurLCMVfixed',Kur)
#stc.save('seg6')
stcSeg=mne.read_source_estimate('seg6-vl.stc')
stcC=stc.crop(stc.times[0], stc.times[0])
stcC.data[:,0]=Kur
# Save result in a 4D nifti file
img = mne.save_stc_as_volume('lcmv_g2.nii', stcC,
                             fwd['src'], mri_resolution=False)