1# -*- coding: utf-8 -*-

"""Widget para actualizar el estado del Turpial"""
#
# Author: Wil Alvarez (aka Satanas)
# Dic 20, 2009

from gi.repository import Gdk, Gtk, GObject

SPELLING = False
try:
    import gtkspell
    SPELLING = True
except:
    pass

from turpial.ui.gtk.waiting import CairoWaiting
from turpial.ui.gtk.friendwin import FriendsWin

class UpdateBox(Gtk.Window):
    def __init__(self, parent):
        GObject.GObject.__init__(self)

        self.what = _('What is happening?')
        self.blocked = False
        self.mainwin = parent
        #self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_title(_('Update status'))
        self.set_resizable(False)
        #self.set_default_size(500, 120)
        self.set_size_request(500, 150)
        self.set_transient_for(parent)
        #self.set_modal(True)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        
        self.label = Gtk.Label()
        self.label.set_use_markup(True)
        self.label.set_alignment(0, 0.5)
        self.label.set_markup('<span size="medium"><b>%s</b></span>' % 
            self.what)
        self.label.set_justify(Gtk.Justification.LEFT)
        
        self.num_chars = Gtk.Label()
        self.num_chars.set_use_markup(True)
        self.num_chars.set_markup('<span size="14000" foreground="#999"><b>140</b></span>')
        
        self.update_text = MessageTextView()
        self.update_text.set_border_width(2)
        self.update_text.set_left_margin(2)
        self.update_text.set_right_margin(2)
        self.update_text.set_wrap_mode(Gtk.WrapMode.WORD)
        buffer = self.update_text.get_buffer()
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.update_text)
        
        updatebox = Gtk.HBox.new(False, 0)
        updatebox.pack_start(scroll, True, True, 3)
        
        self.url = Gtk.Entry()
        self.btn_url = Gtk.Button(_('Shorten URL'))
        self.btn_url.set_tooltip_text(_('Shorten URL'))
        
        tools = Gtk.HBox.new(False, 0)
        tools.pack_start(self.url, True, True, 3)
        tools.pack_start(self.btn_url, False, False, 0)
        
        self.toolbox = Gtk.Expander()
        self.toolbox.set_label(_('Options'))
        self.toolbox.set_expanded(False)
        self.toolbox.add(tools)
        
        self.btn_clr = Gtk.Button()
        self.btn_clr.set_image(self.mainwin.load_image('action-clear.png'))
        self.btn_clr.set_tooltip_text(_('Clear all') + ' (Ctrl+L)')
        self.btn_clr.set_relief(Gtk.ReliefStyle.NONE)
        
        self.btn_frn = Gtk.Button()
        self.btn_frn.set_image(self.mainwin.load_image('action-add-friends.png'))
        self.btn_frn.set_tooltip_text(_('Add friends') + ' (Ctrl+F)')
        self.btn_frn.set_relief(Gtk.ReliefStyle.NONE)
        
        self.btn_upd = Gtk.Button(_('Tweet'))
        self.btn_upd.set_tooltip_text(_('Update your status') + ' (Ctrl+T)')
        chk_short = Gtk.CheckButton(_('Autoshort URLs'))
        chk_short.set_sensitive(False)
        
        top = Gtk.HBox.new(False, 0)
        top.pack_start(self.label, True, True, 5)
        top.pack_start(self.num_chars, False, False, 5)
        
        self.waiting = CairoWaiting(parent)
        self.lblerror = Gtk.Label()
        self.lblerror.set_use_markup(True)
        error_align = Gtk.Alignment.new(0, 0, 0, 0)
        error_align.add(self.lblerror)
        
        buttonbox = Gtk.HBox.new(False, 0)
        #buttonbox.pack_start(chk_short, False, False, 0)
        buttonbox.pack_start(self.btn_frn, False, False, 0)
        buttonbox.pack_start(self.btn_clr, False, False, 0)
        buttonbox.pack_start(Gtk.HSeparator(), False, False, 2)
        buttonbox.pack_start(self.btn_upd, False, False, 0)
        abuttonbox = Gtk.Alignment.new(1, 0.5, 0, 0)
        abuttonbox.add(buttonbox)
        
        bottom = Gtk.HBox.new(False, 0)
        bottom.pack_start(self.waiting, False, False, 5)
        bottom.pack_start(error_align, True, True, 4)
        bottom.pack_start(abuttonbox, True, True, 5)
        
        vbox = Gtk.VBox.new(False, 0)
        vbox.pack_start(top, False, False, 2)
        vbox.pack_start(updatebox, True, True, 2)
        # vbox.pack_start(bottom, False, False, 2)
        vbox.pack_start(self.toolbox, False, False, 2)
        
        self.add(vbox)
        
        self.connect('key-press-event', self.__detect_shortcut)
        self.connect('delete-event', self.__unclose)
        buffer.connect('changed', self.count_chars)
        self.btn_frn.connect('clicked', self.show_friend_dialog)
        self.btn_clr.connect('clicked', self.clear)
        self.btn_upd.connect('clicked', self.update)
        self.btn_url.connect('clicked', self.short_url)
        self.toolbox.connect('activate', self.show_options)
        self.update_text.connect('mykeypress', self.__on_key_pressed)
        
        if SPELLING: 
            try:
                self.spell = gtkspell.Spell (self.update_text)
            except Exception, e_msg:
                # FIXME: Usar el log
                print 'DEBUG:UI:Can\'t load gtkspell -> %s' % e_msg
        else:
            # FIXME: Usar el log
            print 'DEBUG:UI:Can\'t load gtkspell'
    
    def __on_key_pressed(self, widget, keyval, keymod):
        if keyval == Gdk.KEY_Return:
            self.update(widget)
        elif keyval == Gdk.KEY_Escape:
            self.__unclose(widget)
        return False
    
    def __detect_shortcut(self, widget, event=None):
        keyname = Gdk.keyval_name(event.keyval)
        
        if (event.get_state() & Gdk.ModifierType.CONTROL_MASK) and keyname.lower() == 'f':
            self.show_friend_dialog(widget)
            return True
        elif (event.get_state() & Gdk.ModifierType.CONTROL_MASK) and keyname.lower() == 'l':
            self.clear(widget)
            return True
        elif (event.get_state() & Gdk.EventMask.CONTROL_MASK) and keyname.lower() == 't':
            self.update(widget)
            return True
        return False
        
    def __unclose(self, widget, event=None):
        if not self.blocked:
            self.done()
        return True
        
    def show_friend_dialog(self, widget):
        pass
        # f = FriendsWin(self, self.add_friend, 
        #     self.mainwin.request_friends_list())
        
    def block(self):
        self.blocked = True
        self.update_text.set_sensitive(False)
        self.toolbox.set_sensitive(False)
        self.btn_clr.set_sensitive(False)
        self.btn_upd.set_sensitive(False)
        self.btn_url.set_sensitive(False)
        self.btn_frn.set_sensitive(False)
        
    def release(self, msg=None):
        self.blocked = False
        self.update_text.set_sensitive(True)
        self.toolbox.set_sensitive(True)
        self.btn_clr.set_sensitive(True)
        self.btn_upd.set_sensitive(True)
        self.btn_url.set_sensitive(True)
        self.btn_frn.set_sensitive(True)
        self.waiting.stop(error=True)
        
        if not msg:
            msg = _('Oh oh... I couldn\'t send the tweet')
        
        self.lblerror.set_markup("<span size='small'>%s</span>" % msg)
        self.set_focus(self.update_text)
        
    def show(self, text, id, user):
        self.in_reply_id = id
        self.in_reply_user = user
        if id != '' and user != '':
            self.label.set_markup('<span size="medium"><b>%s %s</b></span>' % 
                (_('In reply to'), user))
        
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.set_focus(self.update_text)
        buffer = self.update_text.get_buffer()
        buffer.set_text(text)
        self.show_all()
        
    def done(self, widget=None, event=None):
        buffer = self.update_text.get_buffer()
        buffer.set_text('')
        self.url.set_text('')
        self.lblerror.set_markup('')
        self.label.set_markup(u'<span size="medium"><b>%s</b></span>' % 
            self.what)
        self.waiting.stop()
        self.toolbox.set_expanded(False)
        self.in_reply_id = None
        self.in_reply_user = None
        self.hide()
        return True
        
    def count_chars(self, widget):
        buffer = self.update_text.get_buffer()
        remain = 140 - buffer.get_char_count()
        
        if remain >= 20:
            color = "#999"
        elif 0 < remain < 20:
            color = "#d4790d"
        else:
            color = "#D40D12"
        
        self.num_chars.set_markup('<span size="14000" foreground="%s"><b>%i</b></span>' % (color, remain))
        
    def clear(self, widget):
        self.update_text.get_buffer().set_text('')
        
    def update(self, widget):
        buffer = self.update_text.get_buffer()
        start, end = buffer.get_bounds()
        tweet = buffer.get_text(start, end)
        if tweet == '': 
            self.waiting.stop(error=True)
            self.lblerror.set_markup("<span size='small'>%s</span>" % 
                _('Hey!... you must write something'))
            return
        elif buffer.get_char_count() > 140:
            self.waiting.stop(error=True)
            self.lblerror.set_markup("<span size='small'>%s</span>" % 
                _('Hey!... that message looks like a testament'))
            return
        
        self.waiting.start()
        self.mainwin.request_update_status(tweet, self.in_reply_id)
        self.block()
        
    def short_url(self, widget):
        self.waiting.start()
        self.mainwin.request_short_url(self.url.get_text(), self.update_shorten_url)
        
    def update_shorten_url(self, short):
        if short.err:
            self.waiting.stop(error=True)
            self.lblerror.set_markup("<span size='small'>%s</span>" % 
                _('Oops... I couldn\'t shrink that URL'))
            return
        buffer = self.update_text.get_buffer()
        end_offset = buffer.get_property('cursor-position')
        start_offset = end_offset - 1
        
        end = buffer.get_iter_at_offset(end_offset)
        start = buffer.get_iter_at_offset(start_offset)
        text = buffer.get_text(start, end)
        
        if (text != ' ') and (start_offset > 0):
            short.response = ' ' + short.response
        
        buffer.insert_at_cursor(short.response)
        self.waiting.stop()
        self.lblerror.set_markup("")
        self.toolbox.set_expanded(False)
        self.set_focus(self.update_text)
        
    def show_options(self, widget, event=None):
        self.url.set_text('')
        self.url.grab_focus()
    
    def add_friend(self, user):
        if user is None: return
        
        buffer = self.update_text.get_buffer()
        end_offset = buffer.get_property('cursor-position')
        start_offset = end_offset - 1
        
        end = buffer.get_iter_at_offset(end_offset)
        start = buffer.get_iter_at_offset(start_offset)
        text = buffer.get_text(start, end)
        
        if (text != ' ') and (start_offset > 0):
            user = ' ' + user
        
        buffer.insert_at_cursor(user)

class MessageTextView(Gtk.TextView):
    '''Class for the message textview (where user writes new messages)
    for chat/groupchat windows'''
    __gsignals__ = dict(mykeypress=(GObject.SIGNAL_RUN_LAST | GObject.SIGNAL_ACTION, None, (int, Gdk.ModifierType)))
        
    def __init__(self):
        GObject.GObject.__init__(self)
        
        self.set_border_width(2)
        self.set_left_margin(2)
        self.set_right_margin(2)
        self.set_wrap_mode(Gtk.WrapMode.WORD)
        self.set_accepts_tab(False)

    def destroy(self):
        import gc
        GObject.idle_add(lambda:gc.collect())

    def clear(self, widget=None):
        self.get_buffer().set_text('')
        
if GObject.pygtk_version < (2, 8, 0):
    GObject.type_register(MessageTextView)

# Gtk.binding_entry_add_signal(MessageTextView, Gdk.KEY_Return, 0, 'mykeypress', int, Gdk.KEY_Return, Gdk.ModifierType, 0)
# Gtk.binding_entry_add_signal(MessageTextView, Gdk.KEY_Escape, 0, 'mykeypress', int, Gdk.KEY_Escape, Gdk.ModifierType, 0)
