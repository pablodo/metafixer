# coding: utf-8
import os

from mutagen import File

def get_files(path):
    path = os.path.abspath(path)
    if os.path.isdir(path):
        data = []
        name = os.path.basename(path)
        for f in os.listdir(path):
            new_path = path + '/' + f
            value = get_files(new_path)
            if value is not None:
                data.append(value)
        return {name: data}
    else:
        ext = os.path.splitext(path)
        if ext[1] not in ['.mp3']:
            return None

        fname = os.path.basename(path)
        doc = {'artist': None, 'album': None, 'title': None}
        try:
            mfile = File(path, easy=True)
            if 'artist' in mfile:
                doc['artist'] = mfile['artist'].pop()
            if 'album' in mfile:
                doc['album'] = mfile['album'].pop()
            if 'title' in mfile:
                doc['title'] = mfile['title'].pop()
        except:
            return None
        return fname


def get_music(path):
    doc = {}
    data = _get_music_files(path)

    for value in data:
        artist = value['artist']
        album = value['artist']
        title = value['title']
        fpath = value['file']
        if artist not in doc:
            doc[artist] = {}
        if album not in doc[artist]:
            doc[artist][album] = []
        if title not in doc[artist][album]:
            doc[artist][album].append({title: fpath})

    import pdb; pdb.set_trace()
    return doc

def _get_music_files(path, data=[]):
    path = os.path.abspath(path)
    if os.path.isdir(path):
        for f in os.listdir(path):
            new_path = path + '/' + f
            value = _get_music_files(new_path)
            if value is not None:
                if isinstance(value, list):
                    data = value
                else:
                    data.append(value)
        return data
    else:
        ext = os.path.splitext(path)
        if ext[1] not in ['.mp3']:
            return None

        doc = {'file': path, 'artist': None, 'album': None, 'title': None}
        try:
            mfile = File(path, easy=True)
            if 'artist' in mfile:
                doc['artist'] = mfile['artist'].pop()
            if 'album' in mfile:
                doc['album'] = mfile['album'].pop()
            if 'title' in mfile:
                doc['title'] = mfile['title'].pop()
        except:
            return None
        return doc


if __name__ == '__main__':
    tree = get_files('/home/qa/Music')
    print tree