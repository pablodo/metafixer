import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

class Processor(object):

    def __init__(self, file_type='mp3'):
        self.file_type = file_type

    def capitalize(self, path):
        try:
            dir_list = os.listdir(path)
            for dir_element in dir_list:
                if dir_element.endswith(self.file_type):
                    self.capitalize(dir_element)
        except OSError:
            music_file = MP3(path, ID3=EasyID3) 
            music_file['artist'][0] = music_file['artist'][0].capitalize()
            music_file['artist'][0] = music_file['artist'][0].strip()
            music_file.save()
