# -*- coding: utf-8 -*-

""" Etiqueta de error de login del Turpial"""
#
# Author: Wil Alvarez (aka Satanas)
# Dic 21, 2009

from gi.repository import Gtk, GObject

class LoginLabel(Gtk.DrawingArea):
    def __init__(self, parent):
        GObject.GObject.__init__(self)

        self.error = None
        self.active = False
        self.timer = None
        self.connect('draw', self.draw)
        self.set_size_request(30, 25)

    def deactivate(self):
        self.error = None
        self.active = False
        self.queue_draw_region(self.get_allocation())

    def set_error(self, error):
        print('In LoginLabel.set_error()')
        print('error: %s' % error)
        self.error = error
        self.active = True
        self.queue_draw_region(self.get_allocation())

    def draw(self, cairo_ctx):
        print('In LoginLabel.draw()')
        print('error: %s' % self.error)
        rect = self.get_allocation()

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
