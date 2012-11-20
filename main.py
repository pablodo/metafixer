#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

import explorer
import autocomplete

class MetaFixer(gtk.Window):

    def __init__(self):
        super(MetaFixer, self).__init__(gtk.WINDOW_TOPLEVEL)

        # Window
        self.connect('destroy', self.destroy)
        self.set_title('Meta Fixer')
        self.set_border_width(10)

        # Label
        self.label = gtk.Label('Buttons')
        self.label.set_alignment(1, 1)
        self.label.show()

        # Tree
        tree = MusicFilesTreeView()

        # Exit button
        self.quit_button = gtk.Button(stock=gtk.STOCK_QUIT)
        self.quit_button.connect('clicked', self.destroy)
        self.quit_button.set_flags(gtk.CAN_DEFAULT)
        self.quit_button.show()

        # Buttons box
        box = gtk.VBox()
        box.pack_start(self.label, expand=False)
        box.pack_end(self.quit_button, expand=False)
        box.show()
        self.buttons_box = box

        # Path text
        path_text = autocomplete.AutocompleteEntry(tree.load)
        
        # Main box
        box2 = gtk.VBox(spacing=5)
        box2.pack_start(tree)
        box2.pack_end(path_text, expand=False)
        box2.show()
        box1 = gtk.HBox(spacing=10)
        box1.pack_start(box2)
        box1.pack_end(self.buttons_box, expand=False, fill=False)
        box1.show()
        self.main_box = box1
        self.add(self.main_box)

        self.set_size_request(300, 400)
        self.show_all()

    def main(self):
        gtk.main()

    def destroy(self, widget, data=None):
        gtk.main_quit()


class MusicFilesTreeView(gtk.ScrolledWindow):

    def __init__(self):
        super(MusicFilesTreeView, self).__init__()
        self.path = '/home/qa/Music'
        self.treeview = gtk.TreeView()
        self.load(self.path)

    def load(self, path):
        self.files = []
        self.path = path

        self.data = explorer.get_music(self.path)
        self.store = gtk.TreeStore(str)
        self._load_treestore(self.data)
        self.treeview.set_model(self.store)
        self.treeview.set_reorderable(True)

        self.tree_view_column = gtk.TreeViewColumn('Column')
        if not len(self.treeview.get_columns()):
            self.treeview.append_column(self.tree_view_column)
        self.cell_renderer = gtk.CellRendererText()
        self.tree_view_column.pack_start(self.cell_renderer, True)
        self.tree_view_column.add_attribute(self.cell_renderer, 'text', 0)
        for child in self.get_children():
            self.remove(child)
        self.add(self.treeview)


    def _load_treestore(self, data, parent=None):
        if isinstance(data, dict):
            for key, value in data.iteritems():
                new_parent = self.store.append(parent, [key])
                self._load_treestore(value, new_parent)
        elif isinstance(data, list):
            for value in data:
                i = self.store.append(parent, [value[0]])
                self.files.append((i, value[1]))
        else:
            self.store.append(parent, [data])


if __name__ == '__main__':
    app = MetaFixer()
    try:
        app.main()
    except KeyboardInterrupt:
        pass


