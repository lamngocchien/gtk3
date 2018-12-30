import gi
import os, urlparse
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, WebKit

web = WebKit.WebView()

def get_source(webobj, frame):
    print "loading..."
    # web = WebKit.WebView()
    x = web.get_main_frame().get_data_source().get_data()
    # print x.str

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
        win = Gtk.Window()
        win.set_default_size(800, 500)

        # web.open("http://google.com")
        uri = 'web/page.html'
        uri = os.path.realpath(uri)
        uri = urlparse.ParseResult('file', '', uri, '', '', '')
        uri = urlparse.urlunparse(uri)
        web.load_uri(uri)
        web.connect("load-finished", get_source)
        win.add(web)
        win.show_all()




window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()