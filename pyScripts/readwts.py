#! /usr/bin/env python
# from http://kurage.nimh.nih.gov/meglab/Meg/Readwts

import sys, getopt, struct

__scriptname = sys.argv[0]

__usage = """[-c n] [-l] wtsfile
Reads SAM .wts files, writes virtual channel weights to stdout (all the
weights for V0, then V1, etc.). -c n means just output channel Vn. The
output is preceeded by a line containing the number of weights per channel
and the number of channels."""

def printerror(s):
	sys.stderr.write("%s: %s\n" % (__scriptname, s))

def printusage():
	sys.stderr.write("usage: %s %s\n" % (__scriptname, __usage))

def parseargs(opt):
	try:
		optlist, args = getopt.getopt(sys.argv[1:], opt)
	except Exception, msg:
		printerror(msg)
		printusage()
		sys.exit(1)
	return optlist, args

optlist, args = parseargs("lc:")

chan = None
label = 0
for opt, arg in optlist:
	if opt == '-c':
		chan = int(arg)
	elif opt == '-l':
		label = 1

if len(args) != 1:
	printusage()
	sys.exit(1)

filename = args[0]
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

if chan is not None:
	if chan < 0 or W <= chan:
		printerror("invalid channel; valid range [0..%d]" % (W-1))
		sys.exit(1)
	print N, 1
else:
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

w = [0] * W
for i in xrange(W):
	fmt = ">%dd" % N
	s = struct.calcsize(fmt)
	buf = wts.read(s)
	w[i] = struct.unpack(fmt, buf)

# Write 'em out.

l = range(W)
if chan is not None:
	l = [chan]
for i in l:
	for j in xrange(N):
		if label and ver == 1:
			print chan_idx[j], w[i][j]
		elif label and ver == 2:
			print labels[j], w[i][j]
		else:
			print w[i][j]
