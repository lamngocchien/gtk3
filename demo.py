#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class StackSidebar(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="application title")
        self.set_default_size(900, 600)
        self.connect("destroy", Gtk.main_quit)

        grid = Gtk.Grid()
        self.add(grid)

        stack = Gtk.Stack()
        stack.set_hexpand(True)
        stack.set_vexpand(True)
        grid.attach(stack, 1, 0, 1, 1)

        stacksidebar = Gtk.StackSidebar()
        stacksidebar.set_stack(stack)
        grid.attach(stacksidebar, 0, 0, 1, 1)

        label = Gtk.Label("label 1 text inside")
        name = "label1"
        title = "label 1 name"
        stack.add_titled(label, name, title)

        label = Gtk.Label("label 2 text inside")
        name = "label2"
        title = "label 2 name"
        stack.add_titled(label, name, title)

        label = Gtk.Label("label 3 text inside")
        name = "label3"
        title = "label 3 name"
        stack.add_titled(label, name, title)

window = StackSidebar()
window.set_wmclass ("application title", "application title")
window.show_all()

Gtk.main()