# -*- coding: utf-8 -*-

"""Widget para mostrar respuestas de un tweet en Turpial"""
#
# Author: Wil Alvarez (aka Satanas)
# Feb 02, 2010

import gobject
from gi.repository import Gdk
from gi.repository import Gtk

from turpial.ui.gtk.columns import SingleColumn

class ConversationBox(Gtk.Window):
    def __init__(self, parent):
        gobject.GObject.__init__(self)
        
        self.working = True
        self.mainwin = parent
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_title(_('In reply to...'))
        self.set_resizable(False)
        self.set_size_request(400, 300)
        self.set_transient_for(parent)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        
        self.tweets = SingleColumn(parent, _('In reply to...'))
        
        top = Gtk.VBox(False, 0)
        top.pack_start(self.tweets, True, True, 0)
        
        self.add(top)
        
        self.connect('delete-event', self.__unclose)
        self.connect('size-request', self.__size_request)
    
    def __size_request(self, widget, event, data=None):
        w, h = self.get_size()
        self.tweets.update_wrap(w)
        
    def __unclose(self, widget, event=None):
        if not self.working:
            self.hide()
        return True
        
    def show(self, twt_id, user):
        self.in_reply_id = twt_id
        self.in_reply_user = user
        self.set_title(_('In reply to %s') % user)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.tweets.clear()
        self.tweets.start_update()
        self.show_all()
        
    def update(self, response):
        self.working = False
        
        if response.type == 'error':
            self.tweets.stop_update(True, response.errmsg)
        else:
            self.tweets.stop_update()
            self.tweets.clear()
            self.tweets.update_tweets(response)

