import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

people = [
    ("One",1,"Mot"),
    ("Two",2,"Hai"),
    ("Three",3,"Ba"),
    ("Four",4,"Bon"),
    ("Five",5,"Nam"),
]

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="First")
        self.set_border_width(10)
        self.set_size_request(300,50)

        #layout
        layout = Gtk.Box()
        self.add(layout)

        # Convert data
        people_list_store = Gtk.ListStore(str,int,str)
        for item in people:
            people_list_store.append(list(item))

        # for row in people_list_store:
        #     # print row[:]
        #     print row[2]

        # Treeview
        people_tree_view = Gtk.TreeView(people_list_store)
        for i , col_title in enumerate(["Name","Age","Profession"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)

            people_tree_view.append_column(column)
        layout.pack_start(people_tree_view, True, True, 0)





window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()