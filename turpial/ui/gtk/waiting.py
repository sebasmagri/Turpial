# -*- coding: utf-8 -*-

# Indicador de progreso del Turpial
#
# Author: Wil Alvarez (aka Satanas)
# Dic 20, 2009

from gi.repository import Gtk, GObject

class CairoWaiting(Gtk.Spinner):
    def __init__(self, parent):
        GObject.GObject.__init__(self)

    def start(self):
        self.show()
        super(CairoWaiting, self).start()

    def stop(self, *args, **kwargs):
        super(CairoWaiting, self).stop()
        self.hide()