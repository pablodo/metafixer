#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pygtk
pygtk.require('2.0')
import gtk

TAB_NEXT = 65289
TAB_PREV = 65056
ENTER = 65293
SHIFT = 65505

class AutocompleteEntry(gtk.Entry):

    def __init__(self, enter_callback=None):
        super(AutocompleteEntry, self).__init__()
        self.connect('key_press_event', self.key_press)
        self.connect('key_release_event', self.key_release)
        self.enter_callback = enter_callback
        self.path = os.getcwd()
        self.set_text(self.path)
        self.path_list = []
        self.number = -1
        self.dirpath = self.path
        self.looking_file = None

    def key_press(self, widget, key):
        if key.keyval in (TAB_NEXT, TAB_PREV):
            if key.keyval == TAB_NEXT:
                self.number += 1
                if self.number >= len(self.path_list):
                    self.number = 0
            elif key.keyval == TAB_PREV:
                self.number -= 1
                if self.number < 0:
                    self.number = len(self.path_list)-1

            if self.number < len(self.path_list):
                new_path = self.dirpath + self.path_list[self.number]
                self.set_text(new_path) 
                self.set_position(len(new_path))

            return True
            
        if key.keyval == ENTER:
            self.enter_callback(self.get_text())
        return False

    def key_release(self, widget, key):
        if key.keyval not in (SHIFT, TAB_NEXT, TAB_PREV, ENTER):
            self._load_path_list(self.get_text())
            if len(self.path_list) == 1 and os.path.isdir(self.path_list[0]):
                self._load_path_list(self.path_list[0])
        return False

    def _load_path_list(self, path):
        path = os.path.abspath(path)
        if os.path.isdir(path) or not '/' in path:
            path += '/'
            self.dirpath = path
            self.looking_file = None
        else:
            self.dirpath, self.looking_file = path.rsplit('/', 1)
            self.dirpath += '/'
        self.path = path
        if not self.dirpath:
            self.dirpath = '/'
        self.number = -1
        self.path_list = []
        try:
            path_list = sorted(os.listdir(self.dirpath))
            for x in path_list:
                if not self.looking_file or x.startswith(self.looking_file):
                    if os.path.isdir(self.dirpath + x):
                        x += '/'
                    self.path_list.append(x)
        except Exception, e:
            print e

    def set_enter_callback(self, callback):
        self.enter_callback = callback
        

