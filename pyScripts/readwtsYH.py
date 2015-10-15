#! /usr/bin/env python
# from http://kurage.nimh.nih.gov/meglab/Meg/Readwts
FIXME - something failed down there

import sys, struct



filename='4/SAM/pnt.txt.wts'
wts = open(filename)

# Read the header.

fmt = ">8s1i"
h = wts.read(struct.calcsize(fmt))
l = struct.unpack(fmt, h)
if l[0] != 'SAMCOEFF':
	printerror("not a SAM wts file")
	sys.exit(1)
ver = l[1]
if ver == 1:
	fmt = ">256s2i4x11d256s3i3i3i2i4x"
elif ver == 2:
	fmt = ">256s2i4x11d256s3i3i3i2i4x3d3d3d32s"
else:
	printerror("unknown SAM wts file format!")
	sys.exit(1)
head = wts.read(struct.calcsize(fmt))
l = struct.unpack(fmt, head)

N = l[1]
W = l[2]
print N, W

# Read the rest of the header.

if ver == 1:
	fmt = ">%di" % N
	s = struct.calcsize(fmt)
	buf = wts.read(s)
	chan_idx = struct.unpack(fmt, buf)
else: # ver == 2
	fmt = ">" + "32s" * (N + W) + "%dd" % (W * 3)
	s = struct.calcsize(fmt)
	buf = wts.read(s)
	l = struct.unpack(fmt, buf)
	labels = [s.split('\x00')[0].split('-')[0] for s in l[:N]]

# Read the weights.
f=open('wts.txt','w')
f.write('%d\n'%W)
f.close()
w = [0] * W
for i in xrange(W):
	fmt = ">%dd" % N
	s = struct.calcsize(fmt)
	buf = wts.read(s)
	w[i] = struct.unpack(fmt, buf)

ww=np.zeros((W,N),float)
for i in xrange(W):
	fmt = ">%dd" % N
	s = struct.calcsize(fmt)
	buf = wts.read(s)
	ww[i,:] = struct.unpack(fmt, buf)

