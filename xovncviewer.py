#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       xovncviewer.py
#       
#       Copyright 2011 Daniel Francis <santiago.danielfrancis@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import gtk
from pygtkvnc.vnc import GRFBWidget
from sugar.activity import activity
from sugar.graphics.toolbutton import ToolButton

class XoVncViewer(activity.Activity):
	def connect_vnc(self, widget):
		builder = gtk.Builder()
		builder.add_from_file("dialog.builder")
		dialog = builder.get_object("Dialog")
		return_ip = ""
		if dialog.run():
			ip = []
			error = 0
			for i in ["p1", "p2", "p3", "p4"]:
				text = builder.get_object(i).get_text()
				if not text:
					error += 1
					break
				ip.append(builder.get_object(i).get_text())
			if not error:
				port = builder.get_object("port_entry").get_text()
				if not port:
					port = 5900
				else:
					port = int(port)
				print ".".join(ip), port
				self.vnc.connect_to_host(".".join(ip), port)
		dialog.destroy()
	
	def fullscreen_cb(self, widget):
		self.fullscreen()
	
	def __init__(self, handle):
		activity.Activity.__init__(self, handle)
		self.toolbox = activity.ActivityToolbox(self)
		activity_toolbar = self.toolbox.get_activity_toolbar()
		activity_toolbar.share.props.visible = False
		activity_toolbar.keep.props.visible = False
		connect = ToolButton("gtk-refresh")
		connect.props.tooltip = "Conectar"
		connect.connect("clicked", self.connect_vnc)
		connect.show()
		activity_toolbar.insert(connect, 2)
		fullscreen = ToolButton("view-fullscreen")
		fullscreen.props.tooltip = "Pantalla Completa"
		fullscreen.connect("clicked", self.fullscreen_cb)
		fullscreen.show()
		activity_toolbar.insert(fullscreen, 2)
		self.set_toolbox(self.toolbox)
		self.toolbox.show()
		area = gtk.ScrolledWindow()
		area.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		area.show()
		self.vnc = GRFBWidget()
		area.add_with_viewport(self.vnc)
		self.vnc.show()
		self.set_canvas(area)
		self.present()
		self.maximize()
		self.show()

if __name__ == "__main__":
	XoVncViewer()
	gtk.main()
