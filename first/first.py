#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi, os, time, re, codecs
from datetime import datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


ProgramName = 'CorePyTools'
ProgramWidth = 500
ProgramHeight = 450

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menuitem action='About' />
  </menubar>
</ui>
"""

def load_configs():
    from os import walk
    mypath = os.getcwd()
    mypath = os.path.join(mypath, "config")
    files = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        files.extend(filenames)
        break
    print files
    json_list = []
    for file in files:
        if file.endswith('.json'):
            json_list.append(file)
    print json_list
    return json_list

class MenuExampleWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title=ProgramName)
        # self.set_default_size(ProgramWidth, ProgramHeight)
        action_group = Gtk.ActionGroup("my_actions")
        self.user_edited_new_document = True
        # File Menu
        action_filemenu = Gtk.Action("FileMenu", "Setting", None, None)
        action_group.add_action(action_filemenu)

        # action_filenew = Gtk.Action("FileNew", "New", None, None)
        # action_filenew.connect("activate", self.on_menu_file_new)
        # action_group.add_action(action_filenew)
        #
        # action_open = Gtk.Action("FileOpen", "Open", None, None)
        # action_open.connect("activate", self.on_menu_file_open)
        # action_group.add_action(action_open)
        #
        # action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        # action_filequit.connect("activate", self.on_menu_file_quit)
        # action_group.add_action(action_filequit)

        # Edit Menu
        # action_filemenu = Gtk.Action("EditMenu", "Edit", None, None)
        # action_group.add_action(action_filemenu)
        #
        # action_filenew = Gtk.Action("EditCopy", "Copy", None, None)
        # action_filenew.connect("activate", self.on_menu_file_new)
        # action_group.add_action(action_filenew)
        #
        # action_open = Gtk.Action("EditPaste", "Paste", None, None)
        # action_open.connect("activate", self.on_menu_file_open)
        # action_group.add_action(action_open)
        #
        # action_filequit = Gtk.Action("EditSomething", "Something", None, None)
        # action_filequit.connect("activate", self.on_menu_file_quit)
        # action_group.add_action(action_filequit)

        # About
        action_about = Gtk.Action("About", " About ", 5, None)
        action_about.connect("activate", self.on_menu_about)
        action_about.set_tooltip('About')
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


        #Main SiderBar
        grid = Gtk.Grid()
        self.add(grid)

        stack = Gtk.Stack()
        stack.set_homogeneous(False)
        stack.set_hexpand(True)
        stack.set_vexpand(True)
        grid.attach(stack, 1, 0, 1, 1)

        stacksidebar = Gtk.StackSidebar()
        stacksidebar.set_stack(stack)
        grid.attach(stacksidebar, 0, 0, 1, 1)




        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_menu = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        box_content_blank =  Gtk.Box(spacing=10)
        box_content_blank.set_size_request(1,15)
        box_content_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_content.pack_start(box_content_blank, False, False, 0)
        box_content.pack_start(box_content_main, False, False, 0)

        # box.pack_start(box_menu, False, False, 0)
        box_menu.pack_start(menubar, False, False, 0)
        box.pack_start(box_content, False, False, 0)

        # label = Gtk.Label("Stack Content on Page %i" % (page))


        # Add button
        # self.add(box)
        stack.add_titled(box, 'Measurement Compare', 'Measurement Compare')

        # layout2 = Gtk.Box(spacing=10)
        # box.add(layout)

        # button 1
        button1 = Gtk.Button("Select Old")
        button1.connect("clicked", self.button_clicked1)
        # button1.set_size_request(120,30)

        # button 2
        button2 = Gtk.Button("Select New")
        button2.connect("clicked", self.button_clicked2)
        # button2.set_size_request(120, 30)


        # Path 1
        self.path1 = Gtk.Entry()
        self.path1.set_property("width-request", 450)
        self.path1.set_text("")
        # Path 2
        self.path2 = Gtk.Entry()
        self.path2.set_property("width-request", 450)
        self.path2.set_text("")


        # Add some config
        layout3 = Gtk.Box(spacing=10)
        layout3.set_homogeneous(False)
        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        # vbox_left.set_properties("width-request", 120)
        vbox_left.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        # vbox_right.set_margin_top(10)
        # vbox_right.set_margin_left(10)
        vbox_right.set_margin_right(10)
        vbox_right.set_homogeneous(False)
        # Make two columns
        layout3.pack_start(vbox_left, True, True, 0)
        layout3.pack_start(vbox_right, True, True, 0)



        # Add to layout
        label1 = Gtk.Label("Old Prompt")
        # label1.set_property("width-request", 120)
        label1.set_justify(Gtk.Justification.RIGHT)

        label2 = Gtk.Label("New Prompt")
        # label2.set_property("width-request", 120)
        label2.set_justify(Gtk.Justification.RIGHT)



        self.first_prompt = Gtk.Entry()
        self.first_prompt.set_property("width-request", 450)
        self.first_prompt.set_text("")

        # Path 2
        self.second_prompt = Gtk.Entry()
        self.second_prompt.set_property("width-request", 450)
        self.second_prompt.set_text("")



        label3 = Gtk.Label("Old Version")
        # label3.set_property("width-request", 120)
        label3.set_justify(Gtk.Justification.RIGHT)

        label4 = Gtk.Label("New Version")
        # label4.set_property("width-request", 120)
        label4.set_justify(Gtk.Justification.RIGHT)



        self.first_version = Gtk.Entry()
        self.first_version.set_property("width-request", 450)
        self.first_version.set_text("")

        # Path 2
        self.second_version = Gtk.Entry()
        self.second_version.set_property("width-request", 450)
        self.second_version.set_text("")

        # vbox_left.pack_start(Gtk.Label(""), True, True, 0)
        # vbox_right.pack_start(Gtk.Label(""), True, True, 7)
        button1.set_margin_top(10)
        self.path1.set_margin_top(10)
        vbox_left.add(button1)
        vbox_right.add(self.path1)
        vbox_left.pack_start(label1, True, True, 0)
        vbox_right.pack_start(self.first_prompt, True, True, 0)
        vbox_left.pack_start(label3, True, True, 0)
        vbox_right.pack_start(self.first_version, True, True, 0)



        # vbox_left.pack_start(Gtk.Label(""), True, True, 0)
        # vbox_right.pack_start(Gtk.Label(""), True, True, 8)
        button2.set_margin_top(10)
        vbox_left.add(button2)
        self.path2.set_margin_top(10)
        vbox_right.add(self.path2)

        vbox_left.pack_start(label2, True, True, 0)
        vbox_right.pack_start(self.second_prompt, True, True, 0)
        vbox_left.pack_start(label4, True, True, 0)
        vbox_right.pack_start(self.second_version, True, True, 0)

        # vbox_left.pack_start(Gtk.Label(""), True, True, 0)
        # vbox_right.pack_start(Gtk.Label(""), True, True, 8)

        label5 = Gtk.Label("Select Config File")
        # label5.set_margin_top(15)
        # label5.set_property("width-request", 120)
        label5.set_justify(Gtk.Justification.RIGHT)
        vbox_left.pack_start(label5, True, True, 0)



        self.config = 'config.json'
        self.configs = load_configs()
        self.config_combo = Gtk.ComboBoxText()
        self.config_combo.set_entry_text_column(0)
        self.config_combo.connect("changed", self.on_config_combo_changed)
        for config in self.configs:
            self.config_combo.append_text(config)

        vbox_right.pack_start(self.config_combo, False, False, 0)

        button_update = Gtk.Button("Reload Config")
        button_update.connect("clicked", self.update_config_file)
        # vbox_right.pack_start(button_update, False, False, True)

        # box_content_main.pack_start(layout1, False, False, 0)
        # box_content_main.pack_start(layout2, False, False, 0)
        # Progress Bar
        # layout1 = Gtk.Box(spacing=10)
        # self.updating = True
        # self.progressbar = Gtk.ProgressBar()
        # layout1.pack_start(self.progressbar, True, True, 0)

        # self.levelbar = Gtk.LevelBar()
        # self.levelbar.set_min_value(0)
        # self.levelbar.set_max_value(100)
        # self.levelbar.set_value(0)

        # layout1.pack_start(self.levelbar, True, True, 0)
        # box_content_main.pack_start(layout1,  False, False, 0)
        # box_content_main.pack_start(layout1,  False, False, 0)
        box_content_main.pack_start(layout3,  False, False, 0)
        # vbox_left.pack_start(Gtk.Label(""), True, True, 0)
        # vbox_right.pack_start(Gtk.Label(""), True, True, 8)


        layout_last = Gtk.Box(spacing=10)
        layout_last.set_margin_right(10)
        layout_last.set_margin_bottom(5)
        button_last = Gtk.Button("Comparasion")
        button_last.connect("clicked", self.button_compare)
        # button_last.set_size_request(120,30)
        label_last = Gtk.Label("")
        label_last.set_property("width-request", 400)
        # label_last.set_property("height-request", 40)
        layout_last.add(label_last)
        layout_last.add(button_update)
        layout_last.add(button_last)
        box_content_main.pack_start(layout_last, False, False, 10)

        self.file_name_default = 'result.xlsx'

        label = Gtk.Label("Under Contruction")
        stack.add_titled(label, 'Configuration Compare', 'Configuration Compare')
        label = Gtk.Label("Under Contruction")
        stack.add_titled(label, 'Excel To Json', 'Excel To Json')
        # label = Gtk.Label("Under Contruction")
        about_box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        about_box.set_homogeneous(False)
        about_box.set_border_width(10)
        # about_box.set_size_request(500,400)
        # about_box.set_margin_top(10)
        # about_box.set_margin_left(10)
        # about_box.set_margin_right(10)
        # about_box.set_margin_bottom(10)
        label = Gtk.Label()
        label.set_text("CorePyTool"
                       "\n_________________________________________________________________"
                       "___________________________________________________________________\n"
                       "\nVersion 1.0.0"
                       "\nDeveloped by lam.chien"
                       "\nPublished on 2 Jan 2019"
                       "\nSupport: Some kind of measurement on (v)MME, (v)GW")
        label.set_justify(Gtk.Justification.LEFT)

        about_box.pack_start(label, False, False, 0)

        stack.add_titled(about_box, 'About', 'About')

    def update_config_file(self, widget):
        print 'Clicked Update Config'
        # self.levelbar.set_value(0)
        self.configs = load_configs()
        self.config_combo.remove_all()
        for config in self.configs:
            self.config_combo.append_text(config)


    def on_config_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.config = model[tree_iter][0]
            print("Selected: config=%s" % self.config)


    def on_timeout(self, user_data):
        """
        Update value on the progress bar
        """
        if self.activity_mode:
            self.progressbar.pulse()
        else:
            new_value = self.progressbar.get_fraction() + 0.01
            print 'new_value: ', new_value
            if new_value > 1:
                new_value = 0
                # self.timeout_id = GObject.timeout_add(9999999999999999999999, self.on_timeout, None)
                self.save_export()
                GObject.source_remove(self.timeout_id)


            self.progressbar.set_fraction(new_value)

        # As this is a timeout function, return True so that it
        # continues to get called
        # self.save_export()
        return self.updating

    def save_export(self):
        # time.sleep(20)
        # self.begin = self.textbuffer.get_start_iter()
        # self.end = self.textbuffer.get_end_iter()
        dialog = Gtk.FileChooserDialog("Save your text file", self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        dialog.set_default_size(800, 400)

        # self.add_filters(dialog)

        Gtk.FileChooser.set_do_overwrite_confirmation(dialog, True)

        if (self.user_edited_new_document):
            Gtk.FileChooser.set_current_name(dialog, self.file_name_default)
        else:
            Gtk.FileChooser.set_filename(dialog, self.old_filename)

        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            filename = Gtk.FileChooser.get_filename(dialog)
            print "This is the filename: " + filename
            self.save_to_file(filename)
        dialog.destroy()

    def button_compare(self, widget):
        now = datetime.today()
        print 'now: ', now
        self.activity_mode = False
        # self.timeout_id = GObject.timeout_add(360, self.on_timeout, None)
        # GObject.source_remove(self.timeout_id)
        print "Compare Final"
        first_version = self.first_version.get_text()
        print 'first_version: ',first_version
        first_prompt = self.first_prompt.get_text()
        print 'first_prompt: ', first_prompt
        second_version = self.second_version.get_text()
        print 'second_version: ', self.second_version.get_text()
        second_prompt = self.second_prompt.get_text()
        print 'second_prompt: ', second_prompt
        path1 = self.path1.get_text()
        print 'path1: ', path1
        path2 = self.path2.get_text()
        print 'path2: ', path2
        config = self.config
        print 'config: ', config
        # fp = open(unicode(path2, "utf-8"))
        fp = open(unicode(path2, "utf-8"))
        for line in fp:
            print line
        self.file_name_default = first_prompt.replace(' ','_') + first_version.replace(' ','_') + '_'
        self.file_name_default += second_prompt.replace(' ','_') + second_version.replace(' ','_')
        self.file_name_default += str(now.year)
        self.file_name_default += str(now.month)
        self.file_name_default += str(now.day)
        self.file_name_default += '.xlsx'


        self.save_export()

    def save_to_file(self, filename):
        self.user_edited_new_document = False
        print "User edited is: " + str(self.user_edited_new_document)
        # function to write the file to computer
        # file = open(filename, "w+")
        # file.write('Hello')
        #
        # file.close()

        # save old filename for later
        # self.old_filename = filename

        import xlsxwriter
        # with open('config.json', 'r') as f:
        #     config = json.load(f)
        # name = config['file_export']

        # print config['data']['file2'][0]
        workbook = xlsxwriter.Workbook(filename + '.xlsx')
        worksheet = workbook.add_worksheet()

        # Some data we want to write to the worksheet.
        expenses = (
            ['Rent', 1000],
            ['Gas', 100],
            ['Food', 300],
            ['Gym', 50],
        )

        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0

        # Iterate over the data and write it out row by row.
        for item, cost in (expenses):
            worksheet.write(row, col, item)
            worksheet.write(row, col + 1, cost)
            row += 1

        # Write a total using a formula.
        worksheet.write(row, 0, 'Total')
        worksheet.write(row, 1, '=SUM(B1:B4)')

        workbook.close()

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()

    def on_menu_file_open(self, widget):
        print("Open on File Menus")

    def on_menu_about(self, widget):
        print("About on File Menus")
        dialog = PopUp(self)
        dialog.set_default_size(400, 75)
        respone = dialog.run()
        if respone == Gtk.ResponseType.OK:
            print "OK"
        elif respone == Gtk.ResponseType.CANCEL:
            print "Cancel"
        dialog.destroy()

    def on_menu_file_new(self, widget):
        print("New on File Menus")

    def button_clicked1(self, widget):
        print "Go to button_clicked1"
        dialog = Gtk.FileChooserDialog("Select a file", self, Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Open", Gtk.ResponseType.OK
                                        )
                                       )
        dialog.set_default_size(800, 400)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print "Open Clicked"
            print ("File: "+dialog.get_filename())
            self.path1.set_text(unicode(dialog.get_filename(), "utf-8"))
            # print ("Path: "+dialog.get_file())
            # fp = open(self.path1.get_text)
            # for line in fp:
            #     print line
        elif response == Gtk.ResponseType.CANCEL:
            print ("Cancel Clicked")
        dialog.destroy()

    def button_clicked2(self, widget):
        print "Go to button_clicked2"
        dialog = Gtk.FileChooserDialog("Select a file", self, Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Open", Gtk.ResponseType.OK
                                        )
                                       )
        dialog.set_default_size(800, 400)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print "Open Clicked"
            print ("File: "+dialog.get_filename())
            self.path2.set_text(unicode(dialog.get_filename(), "utf-8"))

            # print ("Path: "+dialog.get_file())
        elif response == Gtk.ResponseType.CANCEL:
            print ("Cancel Clicked")
        dialog.destroy()


class PopUp(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "About", parent, Gtk.DialogFlags.MODAL, (
            # "Custom cancel text", Gtk.ResponseType.CANCEL,
            # Gtk.STOCK_OK, Gtk.ResponseType.OK,
        ))
        self.set_border_width(10)
        self.set_size_request(300, 100)
        area = self.get_content_area()
        area.add(Gtk.Label("Measurement Compare Tool for Performance Team\nVersion 1.0.0\nDeveloped by lam.chien\nPublished on 2 Jan 2019"
                           "\nSupport: Some kind of measurement on (v)MME, (v)GW"))
        self.show_all()


window = MenuExampleWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()