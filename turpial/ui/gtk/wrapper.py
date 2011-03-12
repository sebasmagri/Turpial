# -*- coding: utf-8 -*-

"""Contenedor genérico para los widgets del Turpial"""
#
# Author: Wil Alvarez (aka Satanas)
# Dic 21, 2009

from gi.repository import GObject, Gtk

class WrapperAlign:
    left = 0
    middle = 1
    right = 2
    
class Wrapper(Gtk.VBox):
    def __init__(self):
        GObject.GObject.__init__(self)
        
        self.children = {
            WrapperAlign.left: None,
            WrapperAlign.middle: None,
            WrapperAlign.right: None,
        }
    
    def _append_widget(self, widget, align):
        self.children[align] = widget
        
    def change_mode(self, mode):
        for child in self.get_children():
            self.remove(child)
        
        if mode == 'wide':
            self.wrapper = Gtk.HBox.new(True, 0)
            
            for i in range(3):
                widget = self.children[i]
                if widget is None:
                    continue
                
                box = Gtk.VBox.new(False, 0)
                #box.pack_start(Gtk.Label(widget.caption, True, True, 0), False, False)
                if widget.get_parent(): 
                    widget.reparent(box)
                else:
                    box.pack_start(widget, True, True)
                self.wrapper.pack_start(box, True, True, 0)
        else:
            self.wrapper = Gtk.Notebook()
            
            for i in range(3):
                widget = self.children[i]
                if widget is None:
                    continue
                
                if widget.get_parent(): 
                    widget.reparent(self.wrapper)
                    self.wrapper.set_tab_label(widget,
                                               Gtk.Label(label=widget.caption))
                else:
                    self.wrapper.append_page(widget, Gtk.Label(label=widget.caption))
                
                # self.wrapper.set_tab_label_packing(widget,
                #                                    True, True, Gtk.PACK_START)

        self.add(self.wrapper)
        self.show_all()
        
    def update_wrap(self, width, mode):
        # Reimplementar en la clase hija de ser necesario
        if mode == 'single':
            w = width
        else:
            w = width / 3
        
        for i in range(3):
            widget = self.children[i]
            if widget is None:
                continue
            
            widget.update_wrap(w)
