"""
plyfun

@author:wronk

Write surface to a .ply (Stanford 3D mesh file) in a way that preserves
vertex order in the MNE sense. Extendable for colors or other vertex/face properties.

.ply format: https://en.wikipedia.org/wiki/PLY_(file_format)
"""

import mne
import numpy as np
from os import path as op
import os
from os import environ


def write_surf2ply(rr, tris, save_path):
    out_file = open(save_path, 'w')

    head_strs = ['ply\n', 'format ascii 1.0\n']
    ele_1 = ['element vertex ' + str(len(rr)) + '\n',
             'property float x\n',
             'property float y\n',
             'property float z\n']
    ele_2 = ['element face ' + str(len(tris)) + '\n',
             'property list uchar int vertex_index\n']
    tail_strs = ['end_header\n']

    # Write Header
    out_file.writelines(head_strs)
    out_file.writelines(ele_1)
    out_file.writelines(ele_2)
    out_file.writelines(tail_strs)

    ##############
    # Write output
    ##############
    # First, write vertex positions
    for vert in rr:
        out_file.write(str(vert[0]) + ' ')
        out_file.write(str(vert[1]) + ' ')
        out_file.write(str(vert[2]) + '\n')

    # Second, write faces using vertex indices
    for face in tris:
        out_file.write(str(3) + ' ')
        out_file.write(str(face[0]) + ' ')
        out_file.write(str(face[1]) + ' ')
        out_file.write(str(face[2]) + '\n')

    out_file.close()


if __name__ == '__main__':
    struct_dir = op.join(environ['SUBJECTS_DIR'])
    subject = 'AKCLEE_139'

    surf_fname = op.join(struct_dir, subject, 'surf', 'lh.pial')
    save_path = op.join('/media/Toshiba/Blender/Brains', subject,
                        'lh.pial_reindex.ply')

    rr, tris = mne.read_surface(surf_fname)
    write_surf2ply(rr, tris, save_path)
