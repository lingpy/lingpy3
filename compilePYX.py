"""
Script handles compilation of Cython files to C and also to C-Extension modules.
"""
import os
import sys
from subprocess import check_call
from io import open


def pyx2py(infile, outfile, debug=False):
    with open(infile, 'r', encoding='utf8') as f:
        data = f.readlines()
    
    words = [
        'bint',
        'int',
        'float',
        'list',
        'str',
        'object',
        'tuple',
        'dict',
        'double',
    ]
    newlines = ['from __future__ import unicode_literals\n']
    for line in data:
        old_line = line
        if 'cdef extern from' in line:
            line = '# [autouncomment] ' + line
            line += 'from math import sqrt\n'
        elif 'double sqrt( double x)' in line:
            line = '# [autouncomment] ' + line
        elif '=' not in line:
            if 'cdef' in line:
                for w in words:
                    if 'cdef ' + w + ' ' in line:
                        line = '# [autouncomment] ' + line
                        break
            else:
                for w in words:
                    if ' ' + w + ' ' in line:
                        line = line.replace(w+' ', '')
                        break
        else:
            if 'cdef' in line:
                for w in words:
                    if 'cdef ' + w + ' ' in line:
                        line = line.replace('cdef ' + w + ' ', '')
                        break
            else:
                for w in words:
                    if ' '+w+' ' in line:
                        line = line.replace(w+' ', '')
                        break
        newlines += [line]
        if old_line != line and debug:
            print(old_line, line)

    with open(outfile, 'w', encoding='utf8') as f:
        f.write(''.join(newlines))


def cython_path(fname):
    return os.path.join('lingpy3', 'algorithm', 'cython', fname)


if __name__ == '__main__':
    for script in ['calign', 'cluster', 'misc', 'malign', 'talign']:
        print('compiling {0}...'.format(script))
        pyx = cython_path(script + '.pyx')
        pyx2py(pyx, cython_path('_{0}.py'.format(script)))
        check_call(['cython', pyx])
        print('... done.')
    sys.exit(0)
