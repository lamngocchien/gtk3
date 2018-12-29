import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="First")
        self.set_border_width(10)
        self.set_size_request(500,200)

        #layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)
        button = Gtk.Button("Popup")
        button.connect("clicked", self.button_clicked)
        vbox.pack_start(button, True, True, 0)

    def button_clicked(self, widget):
        print "Hello"
        dialog = PopUp(self)
        respone = dialog.run()

        if respone == Gtk.ResponseType.OK:
            print "OK"
        elif respone == Gtk.ResponseType.CANCEL:
            print "Cancel"
        dialog.destroy()

class PopUp(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "PopUp", parent, Gtk.DialogFlags.MODAL, (
            "Custom cancel text", Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK,
        ))
        self.set_border_width(10)
        self.set_size_request(200, 100)
        area = self.get_content_area()
        area.add(Gtk.Label("Wow, this popup is so amazing"))
        self.show_all()

window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()