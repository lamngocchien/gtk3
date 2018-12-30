import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, WebKit
# from gi.repository import Gtk, Gdk
import os, urlparse
def get_source(webobj, frame):
    print "loading..."
    x = web.get_main_frame().get_data_source().get_data()
    print x.str

win = Gtk.Window()
win.set_default_size(500, 400)
web = WebKit.WebView()
# web.open("http://google.com")

uri = 'web/page.html'
uri = os.path.realpath(uri)
uri = urlparse.ParseResult('file', '', uri, '', '', '')
uri = urlparse.urlunparse(uri)
web.load_uri(uri)

# web.open("http://google.com")
web.connect("load-finished", get_source)

win.add(web)

win.show_all()

Gtk.main()