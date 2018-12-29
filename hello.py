import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="First Program")
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        checkbutton = Gtk.CheckButton("Click me1!")
        stack.add_titled(checkbutton, "check", "Check Button")

        # stack1 = Gtk.Stack()
        # stack1.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        # stack1.set_transition_duration(1000)
        # checkbutton2 = Gtk.CheckButton("Click me2!")
        # stack.add_titled(checkbutton2, "check", "Check Button")
        #
        # stack2 = Gtk.Stack()
        # stack2.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        # stack2.set_transition_duration(1000)
        # checkbutton3 = Gtk.CheckButton("Click me3!")
        # stack.add_titled(checkbutton3, "check", "Check Button")

        label = Gtk.Label()
        label.set_markup("<big>A fancy label</big>")
        stack.add_titled(label, "label", "A label")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)


        button = Gtk.Button.new_with_label("Click Me")
        button.connect("clicked", self.on_click_me_clicked)
        vbox.pack_start(button, True, True, 10)


    def on_click_me_clicked(self, button):
        print("\"Click me\" button was clicked")
    def on_hello_clicked(self, button):
        print("\"Click Hello\" button was clicked")
    def on_open_clicked(self, button):
        print("\"Open\" button was clicked")

    def on_close_clicked(self, button):
        print("Closing application")
        Gtk.main_quit()

win = ButtonWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()