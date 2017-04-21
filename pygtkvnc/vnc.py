#!/usr/bin/python
#
# Copyright (C) 2006  Daniel Berrange
# Copyright (C) 2006 Red Hat
#
##  This is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 2 of the License, or
##  (at your option) any later version.
##
##  This software is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this software; if not, write to the Free Software
##  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307,
##  USA.


import gobject
import rfb
import sys
from struct import pack
import pygtk
import gtk

stderr = sys.stderr

from time import time

#host = "courgette"
host = "192.168.1.100"
port = 5900

class GRFBFrameBuffer(rfb.RFBFrameBuffer, gobject.GObject):
    __gsignals__= {
        "resize": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, [int,int]),
        "invalidate": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, [int,int,int,int])
        }

    def __init__(self, canvas):
        self.__gobject_init__()
        self.canvas = canvas
        self.pixmap = None

    def get_pixmap(self):
        return self.pixmap

    def init_screen(self, width, height, name):
        self.pixmap = gtk.gdk.Pixmap(self.canvas.window, width, height)

        self.emit("resize", width, height)
        return (0, 0, width, height)

    def process_pixels(self, x, y, width, height, data):
        if self.pixmap == None:
            return

        gc = self.pixmap.new_gc()
        self.pixmap.draw_rgb_32_image(gc, x, y, width, height, gtk.gdk.RGB_DITHER_NONE, data)
        self.emit("invalidate", x, y, width, height)


    def process_solid(self, x, y, width, height, color):
        print >>stderr, 'process_solid: %dx%d at (%d,%d), color=%r' % (width,height,x,y, color)

    def update_screen(self, t):
        #print >>stderr, 'update_screen'
        pass

    def change_cursor(self, width, height, data):
        print >>stderr, 'change_cursor'

    def move_cursor(self, x, y):
        print >>stderr, 'move_cursor'

gobject.type_register(GRFBFrameBuffer)


class GRFBNetworkClient(rfb.RFBNetworkClient):

    def __init__(self, host, port, converter):
        rfb.RFBNetworkClient.__init__(self, host, port, converter)

        self.watch = None

    def init(self):
        rfb.RFBNetworkClient.init(self)
        self.watch = gobject.io_add_watch(self.sock.fileno(), gobject.IO_IN | gobject.IO_ERR | gobject.IO_HUP, self.handle_io)

    def handle_io(self, src, condition):
        self.loop1()
        return 1

    def close(self):
        rfb.RFBNetworkClient.close(self)

        gobject.source_remove(self.watch)
        self.watch = None

    def update_key(self, down, key):
        self.send(pack('>BBHI', 4, down, 0, key))

    def update_pointer(self, mask, x, y):
        self.send(pack('>BBHH', 5, mask, x, y))

class GRFBWidget(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)

        self.fb = GRFBFrameBuffer(self)
        self.client = None
        
        self.fb.connect("resize", self.resize_display)
        self.fb.connect("invalidate", self.repaint_region)

        self.connect("expose-event", self.expose_region)

	self.connect("motion-notify-event", self.update_pointer)
	self.connect("button-press-event", self.update_pointer)
	self.connect("button-release-event", self.update_pointer)
	self.connect("key-press-event", self.key_press)
	self.connect("key-release-event", self.key_release)

        self.set_events(gtk.gdk.EXPOSURE_MASK |
                        gtk.gdk.LEAVE_NOTIFY_MASK |
                        gtk.gdk.ENTER_NOTIFY_MASK |
                        gtk.gdk.KEY_RELEASE_MASK |
                        gtk.gdk.KEY_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.POINTER_MOTION_HINT_MASK)

        self.set_property("can-focus", True)

    def connect_to_host(self, host, port):
        if self.client != None:
            self.disconnect_from_host()
        
        self.client = GRFBNetworkClient(host, port, self.fb)

        self.client.init()
        self.client.auth()
        self.client.start()
        self.client.request_update()

    def disconnect_from_host(self):
        if self.client == None:
            return
        self.client.close()
        self.client = None

    def state_to_mask(self, state):
        mask = 0
        if state & gtk.gdk.BUTTON1_MASK:
            mask = mask + 1
        if state & gtk.gdk.BUTTON2_MASK:
            mask = mask + 2
        if state & gtk.gdk.BUTTON3_MASK:
            mask = mask + 4
        if state & gtk.gdk.BUTTON4_MASK:
            mask = mask + 8
        if state & gtk.gdk.BUTTON5_MASK:
            mask = mask + 16

        return mask

    def update_pointer(self, win, event):
        x, y, state = event.window.get_pointer()
        self.client.update_pointer(self.state_to_mask(state), x, y)
        return True

    def key_press(self, win, event):
        self.client.update_key(1, event.keyval)
        return True
    
    def key_release(self, win, event):
        self.client.update_key(0, event.keyval)
        return True

    def get_frame_buffer(self):
        return self.fb

    def resize_display(self, fb, width, height):
        self.set_size_request(width, height)


    def repaint_region(self,fb, x, y, width, height):
        if self.fb.get_pixmap() == None:
            return
        gc = self.window.new_gc()
        self.window.draw_drawable(gc, self.fb.get_pixmap(), x, y, x, y, width, height)

    def expose_region(self, win, event):
        if self.fb.get_pixmap() == None:
            return
        gc = self.window.new_gc()
        self.window.draw_drawable(gc, self.fb.get_pixmap(), event.area.x, event.area.y, event.area.x, event.area.y, event.area.width, event.area.height)
        color = gtk.gdk.Color()
	pix_data = """/* XPM */
static char * invisible_xpm [] = {
"1 1 1 1",
" c None",
" "};"""
        pix = gtk.gdk.pixmap_create_from_data(None, pix_data, 1, 1, 1, color, color)
        invisible = gtk.gdk.Cursor(pix, pix, color, color, 0, 0)
        self.window.set_cursor(invisible)

def main():
    
    win = gtk.Window()
    win.set_name("VNC")
    win.connect("destroy", lambda w: gtk.main_quit())

    pane = gtk.ScrolledWindow()
    pane.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    win.add(pane)
    pane.show()

    vp = gtk.Viewport()
    pane.add(vp)
    vp.show()
    
    vnc = GRFBWidget()
    vp.add(vnc)
    vnc.show()

    win.present()

    vnc.connect_to_host(host, port)

    rootWidth = gtk.gdk.screen_width()
    rootHeight = gtk.gdk.screen_height()

    vncWidth, vncHeight = vnc.get_size_request()

    if vncWidth > (rootWidth-200):
        vncWidth = rootWidth - 200
    if vncHeight > (rootHeight-200):
        vncHeight = rootHeight - 200
    
    vp.set_size_request(vncWidth+2, vncHeight+2)
    gtk.main()
    vnc.disconnect_from_host()

if __name__ == '__main__':
    main()
