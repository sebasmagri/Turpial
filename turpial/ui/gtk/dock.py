# -*- coding: utf-8 -*-

# Dock para los botones principales del Turpial
#
# Author: Wil Alvarez (aka Satanas)
# Dic 20, 2009

import gobject
from gi.repository import Gtk

from turpial.ui.gtk.about import About

class Dock(Gtk.Alignment):
    def __init__(self, parent, mode='single'):
        gobject.GObject.__init__(self)
        
        self.mainwin = parent
        
        self.btn_home = Gtk.Button()
        self.btn_home.set_relief(Gtk.ReliefStyle.NONE)
        self.btn_home.set_tooltip_text(_('Timeline, replies and others'))
        
        self.btn_profile = Gtk.Button()
        self.btn_profile.set_relief(Gtk.ReliefStyle.NONE)
        self.btn_profile.set_tooltip_text(_('Profile, favorites, search'))
        
        self.btn_follow = Gtk.Button()
        self.btn_follow.set_relief(Gtk.ReliefStyle.NONE)
        self.btn_follow.set_tooltip_text(_('Follow People'))
        
        self.btn_update = Gtk.Button()
        self.btn_update.set_relief(Gtk.ReliefStyle.NONE)
        self.btn_update.set_tooltip_text(_('Update status'))
        
        self.btn_upload = Gtk.Button()
        self.btn_upload.set_relief(Gtk.ReliefStyle.NONE)
        self.btn_upload.set_tooltip_text(_('Upload image'))
        
        self.btn_settings = Gtk.Button()
        self.btn_settings.set_relief(Gtk.ReliefStyle.NONE)
        self.btn_settings.set_tooltip_text(_('Preferences'))
        
        self.btn_about = Gtk.Button()
        self.btn_about.set_relief(Gtk.ReliefStyle.NONE)
        self.btn_about.set_tooltip_text(_('About Turpial'))
        
        self.btn_home.connect('clicked', self.mainwin.show_home)
        self.btn_follow.connect('clicked', self.show_follow)
        self.btn_update.connect('clicked', self.show_update)
        self.btn_upload.connect('clicked', self.show_upload)
        self.btn_profile.connect('clicked', self.mainwin.show_profile)
        self.btn_settings.connect('clicked', self.mainwin.show_preferences)
        self.btn_about.connect('clicked', self.__show_about)
        
        box = Gtk.HBox()
        box.pack_start(self.btn_home, False, False, 0)
        box.pack_start(self.btn_profile, False, False, 0)
        box.pack_start(self.btn_follow, False, False, 0)
        box.pack_start(self.btn_update, False, False, 0)
        box.pack_start(self.btn_upload, False, False, 0)
        box.pack_start(self.btn_settings, False, False, 0)
        box.pack_start(self.btn_about, False, False, 0)
        
        self.change_mode(mode)
        self.add(box)
        self.show_all()
        
    def __show_about(self, widget):
        about = About(self.mainwin)
        
    def show_follow(self, widget):
        self.mainwin.show_follow_box()
        
    def show_update(self, widget):
        self.mainwin.show_update_box()
        
    def show_upload(self, widget):
        self.mainwin.show_uploadpic_box()
        
    def change_mode(self, mode):
        self.btn_home.set_image(self.mainwin.load_image('dock-home.png'))
        self.btn_update.set_image(self.mainwin.load_image('dock-update.png'))
        self.btn_follow.set_image(self.mainwin.load_image('dock-follow.png'))
        self.btn_upload.set_image(self.mainwin.load_image('dock-uploadpic.png'))
        self.btn_profile.set_image(self.mainwin.load_image('dock-profile.png'))
        self.btn_settings.set_image(self.mainwin.load_image('dock-settings.png'))
        self.btn_about.set_image(self.mainwin.load_image('dock-about.png'))
        return
