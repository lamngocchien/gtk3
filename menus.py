import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='FileNew' />
      <separator />
      <menuitem action='FileOpen' />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='EditMenu'>
      <menuitem action='EditCopy' />
      <menuitem action='EditPaste' />
      <menuitem action='EditSomething' />
    </menu>
    <menuitem action='About' />
  </menubar>
</ui>
"""

class MenuExampleWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Menu")

        self.set_default_size(800, 500)

        action_group = Gtk.ActionGroup("my_actions")


        # File Menu
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filenew = Gtk.Action("FileNew", "New", None, None)
        action_filenew.connect("activate", self.on_menu_file_new)
        action_group.add_action(action_filenew)

        action_open = Gtk.Action("FileOpen", "Open", None, None)
        action_open.connect("activate", self.on_menu_file_open)
        action_group.add_action(action_open)

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)

        # Edit Menu
        action_filemenu = Gtk.Action("EditMenu", "Edit", None, None)
        action_group.add_action(action_filemenu)

        action_filenew = Gtk.Action("EditCopy", "Copy", None, None)
        action_filenew.connect("activate", self.on_menu_file_new)
        action_group.add_action(action_filenew)

        action_open = Gtk.Action("EditPaste", "Paste", None, None)
        action_open.connect("activate", self.on_menu_file_open)
        action_group.add_action(action_open)

        action_filequit = Gtk.Action("EditSomething", "Something", None, None)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)

        # About
        action_about = Gtk.Action("About", "About", None, None)
        action_about.connect("activate", self.on_menu_about)
        action_group.add_action(action_about)
        # End



        # uimanager = self.create_ui_manager()
        uimanager = Gtk.UIManager()

        # Throws exception if something went wrong
        uimanager.add_ui_from_string(UI_INFO)

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)



        uimanager.insert_action_group(action_group)

        menubar = uimanager.get_widget("/MenuBar")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(menubar, False, False, 0)



        self.add(box)

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()

    def on_menu_file_open(self, widget):
        print("Open on File Menus")

    def on_menu_about(self, widget):
        print("About on File Menus")

    def on_menu_file_new(self, widget):
        print("New on File Menus")

window = MenuExampleWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()