# -*- coding: utf-8 -*-

# Indicador de progreso del Turpial
#
# Author: Wil Alvarez (aka Satanas)
# Dic 20, 2009

from gi.repository import Gtk, GObject

class CairoWaiting(Gtk.DrawingArea):
    def __init__(self, parent):
        GObject.GObject.__init__(self)
        self.par = parent
        self.active = False
        self.error = False
        self.connect('draw', self.draw)
        self.set_size_request(16, 16)
        self.timer = None
        self.count = 1
    
    def start(self):
        self.active = True
        self.error = False
        self.timer = GObject.timeout_add(30, self.update)
        self.queue_draw()
        
    def stop(self, error=False):
        self.active = error
        self.error = error
        self.queue_draw()
        if self.timer is not None: GObject.source_remove(self.timer)

    def update(self):
        self.count += 1
        if self.count > 31: self.count = 1
        self.queue_draw()
        return True

    # http://git.gnome.org/browse/pygobject/tree/demos/gtk-demo/demos/drawingarea.py

    def draw(self, cairo_ctx):
        rect = self.get_allocation()

        if not self.active: return
        
        if self.error:
            img = 'wait-error.png'
        else:
            img = 'wait%i.png' % (self.count + 1)
        pix = self.par.load_image(img, True)
        Gdk.cairo_rectangle(cairo_ctx, rect)
        cairo_ctx.set_source_pixbuf(pix, 0, 0)
        cairo_ctx.paint()
        del pix
