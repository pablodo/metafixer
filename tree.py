# coding: utf-8
import sys
import os

from mutagen import File

LINES = {'VH': u'├──',
         'V': u'│',
         'VE': u'└──'}

path = './'
if len(sys.argv) > 1:
    path = sys.argv[1]

def printdir(path, n=0, char=''):
    dirlist = os.listdir(path)
    for index in range(0, len(dirlist)):
        dirname = dirlist[index]
        new_path = path + dirname
        if is_dir(new_path):
            new_path += '/'
            if n == 0:
                print dirname
            else:
                char = LINES['V']
                if index == len(dirlist)-1:
                    char = LINES['VE']
                line = (char + ' ' * 4) * (n-1)
            printdir(new_path, n+1, char)
        else:
            mfile = File(path, easy=True)
            artist = ''
            title = ''
            if 'artist' in mfile:
                artist = mfile['artist'][0]
            if 'title' in mfile:
                title = mfile['title'][0]
            line = '%s - %s' % (artist, title)
            print get_line(line, n, char)


def get_line(path, n, char=''):
#   import pdb; pdb.set_trace()
    line = path
    if n != 0:
        line = ' ' * 4 * n 
    if char != '':
       line += char + u'─' * 4
    if n != 0:
        line = ' ' * 4 * n 
        line = u'│' + line
        line += '%s' % path
    return line
    

def is_dir(path):
    try:
        os.listdir(path)
        return True
    except OSError:
        return False

try:
    printdir(path)
except KeyboardInterrupt:
    pass
