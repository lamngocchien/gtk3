import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="First")
        self.set_border_width(10)
        self.set_size_request(500,200)

        layout = Gtk.Box(spacing = 6)
        self.add(layout)

        button = Gtk.Button("Upload")
        button.connect("clicked", self.button_clicked)
        layout.add(button)

    def button_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Select a file", self, Gtk.FileChooserAction.SELECT_FOLDER,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Open", Gtk.ResponseType.OK
                                        )
                                       )
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print "Open Clicked"
            print ("File: "+dialog.get_filename())
            # print ("Path: "+dialog.get_file())
        elif response == Gtk.ResponseType.CANCEL:
            print ("Cancel Clicked")

        dialog.destroy()

window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()