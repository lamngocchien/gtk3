"""
This simple app allows the user to write some text.
Then click the button to save that text somewhere.
"""

# !/usr/env/python
from gi.repository import Gtk


class TextWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Mini Writer")

        # variable to check if we need to use old filename
        self.user_edited_new_document = True

        self.set_size_request(200, 200)
        table = Gtk.Table(2, 1, True)
        self.add(table)

        textview = Gtk.TextView()
        self.textbuffer = textview.get_buffer()
        table.attach(textview, 0, 1, 0, 1)

        button = Gtk.Button(label="Save As..")
        button.connect("clicked", self.button_pressed)
        table.attach(button, 0, 1, 1, 2, ypadding=5)

    def add_filters(self, dialog):
        # Add text file filter
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text Files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

    def button_pressed(self, button):
        self.begin = self.textbuffer.get_start_iter()
        self.end = self.textbuffer.get_end_iter()
        dialog = Gtk.FileChooserDialog("Save your text file", self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        dialog.set_default_size(800, 400)

        self.add_filters(dialog)

        Gtk.FileChooser.set_do_overwrite_confirmation(dialog, True)

        if (self.user_edited_new_document):
            Gtk.FileChooser.set_current_name(dialog, "Untitled document")
        else:
            Gtk.FileChooser.set_filename(dialog, self.old_filename)

        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            filename = Gtk.FileChooser.get_filename(dialog)
            print "This is the filename: " + filename
            self.save_to_file(filename)

        dialog.destroy()

    def save_to_file(self, filename):
        self.user_edited_new_document = False
        print "User edited is: " + str(self.user_edited_new_document)
        # function to write the file to computer
        file = open(filename, "w+")
        file.write(self.textbuffer.get_text(self.begin, self.end, False))

        file.close()

        # save old filename for later
        self.old_filename = filename


win = TextWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()