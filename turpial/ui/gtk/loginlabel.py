# -*- coding: utf-8 -*-

""" Etiqueta de error de login del Turpial"""
#
# Author: Wil Alvarez (aka Satanas)
# Dic 21, 2009

from gi.repository import Gtk, GObject

class LoginLabel(Gtk.DrawingArea):
    def __init__(self, parent):
        GObject.GObject.__init__(self)
        self.par = parent
        self.error = None
        self.active = False
        self.timer = None
        self.connect('draw', self.draw)
        self.set_size_request(30, 25)
    
    def deactivate(self):
        #if self.timer:
        #    GObject.source_remove(self.timer)
        self.error = None
        self.active = False
        self.queue_draw()
        
    def set_error(self, error):
        self.error = error
        self.active = True
        #if self.timer:
        #    GObject.source_remove(self.timer)
        #self.timer = GObject.timeout_add(5000, self.deactivate)
        self.queue_draw()

    def draw(self, cairo_ctx):
        rect = self.get_allocation()
        
        Gdk.cairo_rectangle(cairo_ctx, rect)
        cairo_ctx.clip()

        if not self.active:
            return

        cairo_ctx.set_source_rgb(0, 0, 0)
        cairo_ctx.fill()
        cairo_ctx.select_font_face('Courier', cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_NORMAL)
        cairo_ctx.set_font_size(12)
        cairo_ctx.set_source_rgb(1, 0.87, 0)
        cairo_ctx.move_to(10, 15)

        cairo_ctx.text_path(self.error)
        cairo_ctx.stroke()
