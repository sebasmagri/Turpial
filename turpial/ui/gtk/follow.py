# -*- coding: utf-8 -*-

# Diálogo para seguir amigos
#
# Author: Wil Alvarez (aka Satanas)
# Jul 07, 2010

from gi.repository import GObject, Gtk

class Follow(Gtk.Window):
    def __init__(self, mainwin, friend=''):
        GObject.GObject.__init__(self)
        
        self.mainwin = mainwin
        self.set_title(_('Follow'))
        self.set_size_request(260, 80)
        self.set_transient_for(mainwin)
        self.set_resizable(False)
        self.set_modal(True)
        self.set_border_width(6)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        
        lbl_user = Gtk.Label(_('User'))
        self.user = Gtk.Entry()
        
        self.btn_ok = Gtk.Button(_('Ok'))
        self.btn_ok.set_can_default(True)
        btn_cancel = Gtk.Button(_('Cancel'))
        
        hbox = Gtk.HBox.new(False, 0)
        hbox.pack_start(lbl_user, False, False, 0)
        hbox.pack_start(self.user, True, True, 0)
        
        box_button = Gtk.HButtonBox()
        box_button.set_spacing(6)
        box_button.set_layout(Gtk.ButtonBoxStyle.END)
        box_button.pack_start(self.btn_ok, True, True, 0)
        box_button.pack_start(btn_cancel, True, True, 0)
        
        vbox = Gtk.VBox.new(False, 0)
        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_start(box_button, False, False, 0)
        
        self.btn_ok.connect('clicked', self.__follow)
        btn_cancel.connect('clicked', self.__close)
        self.user.connect('activate', self.__follow)
        self.connect('delete-event', self.__close)
        
        self.add(vbox)
        self.show_all()
        self.btn_ok.grab_default()
        self.set_default(self.btn_ok)
        self.user.set_text(friend)
        self.user.select_region(0, -1)
        
    def __close(self, widget, event=None):
        self.destroy()
    
    def __follow(self, widget):
        user = self.user.get_text()
        if user != '':
            self.mainwin.request_follow(user)
        self.__close(widget)
        
