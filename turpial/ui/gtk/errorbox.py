# -*- coding: utf-8 -*-

# Widget para mostrar una mensaje de error embebido en Turpial
#
# Author: Wil Alvarez (aka Satanas)
# Jun 26, 2010

from gi.repository import Gdk
from gi.repository import Gtk
import gobject

class ErrorBox(Gtk.HBox):
    def __init__(self, padding=0):
        gobject.GObject.__init__(self)
        
        self.timer = None
        
        self.message = Gtk.Label()
        self.message.set_use_markup(True)
        self.message.set_markup("")
        
        lblalign = Gtk.Alignment.new(0, 0.5, 0, 0)
        lblalign.add(self.message)
        
        ttcolor = Gdk.color_parse('#ebeab8')[1]
        errorevent = Gtk.EventBox()
        errorevent.add(lblalign)
        errorevent.modify_bg(Gtk.StateType.NORMAL, ttcolor)
        errorevent.set_border_width(1)
        
        ttcolor = Gdk.color_parse('#a88f53')[1]
        errorevent2 = Gtk.EventBox()
        errorevent2.add(errorevent)
        errorevent2.modify_bg(Gtk.StateType.NORMAL, ttcolor)
        
        self.btn_close = Gtk.Button()
        self.btn_close.set_relief(Gtk.ReliefStyle.NONE)
        
        self.pack_start(errorevent2, True, True, padding)
        #self.pack_start(self.btn_close, False, False, padding)
        
        errorevent.connect('button-release-event', self.close)
        self.connect('draw', self.draw)
        
    def __show(self, widget=None, event=None):
        if self.message.get_label() == '':
            self.hide()
        else:
            Gtk.HBox.show_all(self)
        
    def draw(self):
        self.__show()
        
    def show_all(self):
        self.__show()
    
    def show_error(self, msg, show=True):
        if show:
            self.message.set_markup(u"<span size='small'>%s</span>" % msg)
            self.timer = gobject.timeout_add(7000, self.close)
            self.show()
        else:
            self.hide()
        
    def hide(self):
        self.message.set_markup("")
        Gtk.HBox.hide(self)
        
    def close(self, widget=None, event=None):
        self.hide()
        if self.timer:
            gobject.source_remove(self.timer)
        
        
