import mne
from os import environ
from shutil import copyfile

#mne.create_default_subject(subject='test4')

subject = 'fsavgsc'
environ["subject"] = subject
freesurfer_home = "/usr/local/freesurfer"
subjects_dir = freesurfer_home + "/subjects"
environ["FREESURFER_HOME"] = freesurfer_home
environ["SUBJECTS_DIR"] = subjects_dir
mne_bin = "/home/yuval/Programs/MNE-2.7.3-3268-Linux-x86_64/bin"
path = environ['PATH']
path = path + ":" + freesurfer_home + "/bin:" + mne_bin
environ['PATH'] = path
ld_lib = environ['LD_LIBRARY_PATH']
ld_lib = ld_lib + ":" + freesurfer_home + "/lib"
environ['LD_LIBRARY_PATH'] = ld_lib
#


# watershed - make BEM model with freesurfer
ws = mne.bem.make_watershed_bem(
    subject=subject, subjects_dir=subjects_dir, overwrite=True)
copyfile(subjects_dir + "/" + subject + "/bem/watershed/" + subject +
         "_inner_skull_surface", subjects_dir + "/" + subject + "/bem/inner_skull.surf")

cd ~/Data/inbal/4temp

# read the data and write as fif

raw = mne.io.bti.read_raw_bti(
    'rs,xc,hb,lf_c,rfhp0.1Hz', rename_channels=False, sort_by_ch_name=False)
raw.save('inbal4temp-raw.fif')


bem_model = mne.make_bem_model(
    subject=subject, subjects_dir=subjects_dir, conductivity=(0.3,))
bem_solution = mne.make_bem_solution(bem_model)
# /usr/local/freesurfer/subjects/aliceIdan/bem
mne.write_bem_solution(
    subjects_dir + "/" + subject + "/bem/" + subject + "-bem.fif", bem_solution)

# check BEM model
mne.viz.plot_bem(subject='aliceIdan',
                 subjects_dir='/usr/local/freesurfer/subjects', orientation='coronal')

# mark fiducials in the GUI, nudge and save
mne.gui.coregistration(
    subject=subject, subjects_dir=subjects_dir, inst='inbal4temp-raw.fif')








# get the digitization data
cd /home/yuval/Data/inbal/4/
raw=mne.io.Raw('4_raw.fif')
dig=raw.info['dig']
fid=dict(LPA=dig[0]['r'],Nz=dig[1]['r'],RPA=dig[2]['r'])
digarray = [dig[digi]['r'].tolist() for digi in range(3,len(dig))]
digarray = [digi['r'].tolist() for digi in dig]
digarray = np.array(digarray)
# get real head size
LRreal=fid['RPA'][0]-fid['LPA'][0]
maxi = np.argmax(digarray[:,2])
ISreal = digarray[maxi,2]
mini = np.argmin(digarray[:,1])
APreal = np.sqrt(np.sum(np.power(digarray[mini,:]-fid['Nz'],2)))
# diplay fiducials + headshape
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Axes3D.scatter(ax, digarray[0,0], digarray[0,1], zs=digarray[0,2],c='r')
Axes3D.scatter(ax, digarray[1,0], digarray[1,1], zs=digarray[1,2],c='g')
Axes3D.scatter(ax, digarray[2,0], digarray[2,1], zs=digarray[2,2],c='b')
Axes3D.scatter(ax, digarray[3:,0], digarray[3:,1], zs=digarray[3:,2],c='k')
plt.show()

# set template head sie
# I took the fiducials from collin 27 after aligning it to MEG space (LPI)
# 'Nasion'      0     98  0
# 'Left Ear'   79.13   4  0
# 'Right Ear'  78.88  -4  0
#  Top  0    0  131
#  Back 0  -92   48
# hence:
# AP = 209mm    sqrt(sum((Back-Temp.fid.fid.pnt(1,:)).^2))
# LR = 166mm    xRight - xLeft
# IS = 169mm    zTop - zLPA
# APtemp = np.sqrt(np.sum(np.power(Back-Nasion,2)))
APtemp = 196
LRtemp = 158
IStemp = 131
# load template brain (collin)
temp=nib.load('/home/yuval/Desktop/T1/ortho.nii')
# change template size
zooms=temp.header.get_zooms()
R = float(LRreal) * 1000.0 / float(LRtemp) * zooms[0]
A = float(APreal) * 1000.0 / float(APtemp) * zooms[1]
S = float(ISreal) * 1000.0 / float(IStemp) * zooms[2]
temp.header.set_zooms([R, A, S])
temp.to_filename('4temp.nii')
# T1.header["pixdim"][1:4] = nii_img.header["pixdim"][1:4]*resize_factor
# nb.save = (nii_img, nii_file_path)
