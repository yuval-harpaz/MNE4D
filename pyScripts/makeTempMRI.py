import nibabel as nib
import mne
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

cd /home/yuval/Data/inbal/4/

raw=mne.io.Raw('4_raw.fif')
dig=raw.info['dig']
fid=dict(LPA=dig[0]['r'],Nz=dig[1]['r'],RPA=dig[2]['r'])
LRreal=fid['RPA'][0]-fid['LPA'][0]

digarray = [dig[digi]['r'].tolist() for digi in range(3,len(dig))]
digarray = [digi['r'].tolist() for digi in dig]
digarray = np.array(digarray)
maxi = np.argmax(digarray[:,2])
ISreal = digarray[maxi,2]
mini = np.argmin(digarray[:,1])
APreal = np.sqrt(np.sum(np.power(digarray[mini,:]-fid['Nz'],2)))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Axes3D.scatter(ax, digarray[0,0], digarray[0,1], zs=digarray[0,2],c='r')
Axes3D.scatter(ax, digarray[1,0], digarray[1,1], zs=digarray[1,2],c='g')
Axes3D.scatter(ax, digarray[2,0], digarray[2,1], zs=digarray[2,2],c='b')
Axes3D.scatter(ax, digarray[3:,0], digarray[3:,1], zs=digarray[3:,2],c='k')
plt.show()

# I took the fiducials from collin 27 like this
# Temp=spm_eeg_inv_mesh([], 2);
# Temp.fid.fid has the fiducials
# Temp.fid.pnt has the scalp
#  Nz    1    85   -41
#  LPA -83   -20   -65
#  RPA  83   -20   -65
#  Top -1.8077  -21.1027  103.9804
#  Back -0.4760 -121.3315   -6.1411
# hence:
# AP = 209mm    sqrt(sum((Back-Temp.fid.fid.pnt(1,:)).^2))
# LR = 166mm    xRight - xLeft
# IS = 169mm    zTop - zLPA

APtemp = 209
LRtemp = 166
IStemp = 169

T1=nib.load('/home/yuval/ft_BIU/matlab/spm8/canonical/single_subj_T1.nii')


zooms=T1.header.get_zooms()
R = float(LRreal) * 1000.0 / float(LRtemp) * zooms[0]
A = float(APreal) * 1000.0 / float(APtemp) * zooms[1]
S = float(ISreal) * 1000.0 / float(IStemp) * zooms[2]
T1.header.set_zooms([R, A, S])
T1.to_filename('4temp.nii')
# T1.header["pixdim"][1:4] = nii_img.header["pixdim"][1:4]*resize_factor
# nb.save = (nii_img, nii_file_path)


T1.to_filename('4temp.hdr')