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
    def draw(self, widget, cairo_ctx, event):
        cairo_ctx.set_line_width(0.8)
        rect = self.get_allocation()

        cairo_ctx.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        cairo_ctx.clip()
        
        cairo_ctx.rectangle(0, 0, rect.width, rect.height)
        if not self.active: return
        
        if self.error:
            img = 'wait-error.png'
        else:
            #img = 'wait2-%i.png' % (self.count + 1)
            img = 'wait%i.png' % (self.count + 1)
        pix = self.par.load_image(img, True)
        cairo_ctx.set_source_pixbuf(pix, 0, 0)
        cairo_ctx.paint()
        del pix
