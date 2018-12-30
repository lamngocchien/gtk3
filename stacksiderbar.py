import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class StackSidebar(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(800, 300)
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

        for page in range(1, 8):
            label = Gtk.Label("Stack Content on Page %i" % (page))
            name = "label%i" % page
            title = "Feature %i" % page
            stack.add_titled(label, name, title)

        about_box = Gtk.Box(spacing=10)
        about_box.set_border_width(10)
        about_box.set_size_request(800, 400)
        about_box.set_homogeneous(False)
        about_box.set_margin_top(10)
        about_box.set_margin_left(10)
        about_box.set_margin_right(10)
        about_box.set_margin_bottom(10)
        label = Gtk.Label()
        label.set_text(
            "Measurement Compare Tool for Performance Team\nVersion 1.0.0\nDeveloped by lam.chien\nPublished on 2 Jan 2019"
            "\nSupport: Some kind of measurement on (v)MME, (v)GW")
        label.set_justify(Gtk.Justification.LEFT)
        # about_box.pack_start(Gtk.Label(""),0, 0, 0)
        about_box.pack_start(label, False, False, 0)
        stack.add_titled(about_box, 'About', 'About')

window = StackSidebar()
window.show_all()

Gtk.main()