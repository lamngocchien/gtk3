#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi, os, time, re, codecs, paramiko, urlparse
from datetime import datetime
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, WebKit
from lib import *

ProgramName = 'CorePyTools'
ProgramWidth = 500
ProgramHeight = 450

def get_source(webobj, frame):
    print "loading..."
    web = WebKit.WebView()
    x = web.get_main_frame().get_data_source().get_data()
    # print x.str

def load_configs():
    from os import walk
    mypath = os.getcwd()
    mypath = os.path.join(mypath, "config")
    files = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        files.extend(filenames)
        break
    # print files
    json_list = []
    for file in files:
        if file.endswith('.json'):
            json_list.append(file)
    # print json_list
    return json_list

class MenuExampleWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title=ProgramName)
        self.set_default_size(ProgramWidth, ProgramHeight)

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

# =========================================================================================================================================
        # Measurement
# =========================================================================================================================================

        # Measurement Compare Tab
        self.user_edited_new_document = True
        self.file_name_default = 'result.xlsx'
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        # box_menu = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        box_content_blank = Gtk.Box(spacing=10)
        box_content_blank.set_size_request(1,15)
        box_content_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_content.pack_start(box_content_blank, False, False, 0)
        box_content.pack_start(box_content_main, False, False, 0)

        # box.pack_start(box_menu, False, False, 0)
        # box_menu.pack_start(menubar, False, False, 0)
        box.pack_start(box_content, False, False, 0)

        stack.add_titled(box, 'Measurement Compare', 'Measurement Compare')

        # button 1
        button1 = Gtk.Button("Select Old")
        button1.connect("clicked", self.measurement_compare_upload1)
        button2 = Gtk.Button("Select New")
        button2.connect("clicked", self.measurement_compare_upload2)

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
        vbox_left.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right.set_margin_right(10)
        vbox_right.set_homogeneous(False)
        # Make two columns
        layout3.pack_start(vbox_left, True, True, 0)
        layout3.pack_start(vbox_right, True, True, 0)

        # Add to layout
        label1 = Gtk.Label("Old Prompt")
        label2 = Gtk.Label("New Prompt")

        self.first_prompt = Gtk.Entry()
        self.first_prompt.set_property("width-request", 450)
        self.first_prompt.set_text("")
        # Path 2
        self.second_prompt = Gtk.Entry()
        self.second_prompt.set_property("width-request", 450)
        self.second_prompt.set_text("")

        label3 = Gtk.Label("Old Version")
        label4 = Gtk.Label("New Version")

        self.first_version = Gtk.Entry()
        self.first_version.set_property("width-request", 450)
        self.first_version.set_text("")

        # Path 2
        self.second_version = Gtk.Entry()
        self.second_version.set_property("width-request", 450)
        self.second_version.set_text("")

        button1.set_margin_top(10)
        self.path1.set_margin_top(10)
        vbox_left.add(button1)
        vbox_right.add(self.path1)
        vbox_left.pack_start(label1, True, True, 0)
        vbox_right.pack_start(self.first_prompt, True, True, 0)
        vbox_left.pack_start(label3, True, True, 0)
        vbox_right.pack_start(self.first_version, True, True, 0)

        button2.set_margin_top(10)
        vbox_left.add(button2)
        self.path2.set_margin_top(10)
        vbox_right.add(self.path2)

        vbox_left.pack_start(label2, True, True, 0)
        vbox_right.pack_start(self.second_prompt, True, True, 0)
        vbox_left.pack_start(label4, True, True, 0)
        vbox_right.pack_start(self.second_version, True, True, 0)

        label5 = Gtk.Label("Select Config File")
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
        box_content_main.pack_start(layout3,  False, False, 0)

        layout_last = Gtk.Box(spacing=10)
        layout_last.set_margin_right(10)
        layout_last.set_margin_bottom(5)
        button_last = Gtk.Button("Measurement Compare")
        button_last.connect("clicked", self.button_measurement_compare)
        label_last = Gtk.Label("")
        label_last.set_property("width-request", 400)
        layout_last.add(label_last)
        layout_last.add(button_update)
        layout_last.add(button_last)
        box_content_main.pack_start(layout_last, False, False, 10)
        # End Measurement Compare Tab

# =========================================================================================================================================
        # Configuration
# =========================================================================================================================================

        # Configuration Compare Tab
        box_config = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_content_config = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        box_content_blank = Gtk.Box(spacing=10)
        box_content_blank.set_size_request(1, 15)
        box_content_main_config = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_content_config.pack_start(box_content_blank, False, False, 0)
        box_content_config.pack_start(box_content_main_config, False, False, 0)
        label = Gtk.Label("Under Combination")
        label.set_margin_top(10)
        box_content_main_config.add(label)
        box_config.pack_start(box_content_config, False, False, 0)

        # button 1
        button1_config = Gtk.Button("Select Old")
        button1_config.connect("clicked", self.config_compare_upload1)
        button2_config = Gtk.Button("Select New")
        button2_config.connect("clicked", self.config_compare_upload2)

        # Path 1
        self.path1_config = Gtk.Entry()
        self.path1_config.set_property("width-request", 450)
        self.path1_config.set_text("")
        # Path 2
        self.path2_config = Gtk.Entry()
        self.path2_config.set_property("width-request", 450)
        self.path2_config.set_text("")

        # Add some config
        layout3_config = Gtk.Box(spacing=10)
        layout3_config.set_homogeneous(False)
        vbox_left_config = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_left_config.set_homogeneous(False)
        vbox_right_config = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right_config.set_margin_right(10)
        vbox_right_config.set_homogeneous(False)
        # Make two columns
        layout3_config.pack_start(vbox_left_config, True, True, 0)
        layout3_config.pack_start(vbox_right_config, True, True, 0)

        # Add to layout
        label1_config = Gtk.Label("Old Prompt")
        label2_config = Gtk.Label("New Prompt")

        self.first_prompt_config = Gtk.Entry()
        self.first_prompt_config.set_property("width-request", 450)
        self.first_prompt_config.set_text("")
        # Path 2
        self.second_prompt_config = Gtk.Entry()
        self.second_prompt_config.set_property("width-request", 450)
        self.second_prompt_config.set_text("")

        label3_config = Gtk.Label("Old Version")
        label4_config = Gtk.Label("New Version")

        self.first_version_config = Gtk.Entry()
        self.first_version_config.set_property("width-request", 450)
        self.first_version_config.set_text("")

        # Path 2
        self.second_version_config = Gtk.Entry()
        self.second_version_config.set_property("width-request", 450)
        self.second_version_config.set_text("")

        button3_config = Gtk.Button("Select Config File")
        button3_config.connect("clicked", self.config_compare_upload3)

        # Path 3
        self.path3_config = Gtk.Entry()
        self.path3_config.set_property("width-request", 450)
        self.path3_config.set_text("")


        vbox_right_config.pack_start(self.path3_config, True, True, 0)
        vbox_left_config.add(button3_config)
        button1_config.set_margin_top(10)
        self.path1_config.set_margin_top(10)


        vbox_right_config.pack_start(self.path1_config, True, True, 0)
        vbox_left_config.add(button1_config)
        vbox_left_config.pack_start(label1_config, True, True, 0)
        vbox_right_config.pack_start(self.first_prompt_config, True, True, 0)
        vbox_left_config.pack_start(label3_config, True, True, 0)
        vbox_right_config.pack_start(self.first_version_config, True, True, 0)

        button2_config.set_margin_top(10)
        button2_config.set_property("width-request", 120)
        vbox_left_config.add(button2_config)
        self.path2_config.set_margin_top(10)
        vbox_right_config.add(self.path2_config)

        vbox_left_config.pack_start(label2_config, True, True, 0)
        vbox_right_config.pack_start(self.second_prompt_config, True, True, 0)
        vbox_left_config.pack_start(label4_config, True, True, 0)
        vbox_right_config.pack_start(self.second_version_config, True, True, 0)



        layout_last_config = Gtk.Box(spacing=0)
        layout_last_config.set_margin_right(10)
        layout_last_config.set_margin_bottom(5)
        button_last_config = Gtk.Button("Configuration Compare")
        button_last_config.connect("clicked", self.button_config_compare)
        label_last_config = Gtk.Label("")
        label_last_config.set_property("width-request", 500)
        layout_last_config.add(label_last_config)

        layout_last_config.add(button_last_config)
        box_content_main_config.pack_start(layout3_config, False, False, 10)
        box_content_main_config.pack_start(layout_last_config, False, False, 0)

        # label = Gtk.Label("Under Contruction")
        stack.add_titled(box_config, 'Configuration Compare', 'Configuration Compare')
        # End Configuration Compare Tab

# =========================================================================================================================================
        # Protocol Compare
# =========================================================================================================================================

        # Protocol Compare Tab
        box_protocol = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_content_protocol = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        box_content_blank = Gtk.Box(spacing=10)
        box_content_blank.set_size_request(1, 15)
        box_content_main_protocol = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_content_protocol.pack_start(box_content_blank, False, False, 0)
        box_content_protocol.pack_start(box_content_main_protocol, False, False, 0)
        label = Gtk.Label("Under Combination")
        label.set_margin_top(10)
        box_content_main_protocol.add(label)
        box_protocol.pack_start(box_content_protocol, False, False, 0)

        # label = Gtk.Label("Under Adding")
        stack.add_titled(box_protocol, 'Protocol Compare', 'Protocol Compare')
        # End Protocol Compare Tab

# =========================================================================================================================================
        # Measurement Graph
# =========================================================================================================================================

        # Protocol Compare Tab
        box_mgraph = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_content_mgraph = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        box_content_blank = Gtk.Box(spacing=10)
        box_content_blank.set_size_request(1, 15)
        box_content_main_mgraph = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_content_mgraph.pack_start(box_content_blank, False, False, 0)
        box_content_mgraph.pack_start(box_content_main_mgraph, False, False, 0)
        label = Gtk.Label("Under Combination")
        label.set_margin_top(10)
        box_content_main_mgraph.add(label)
        box_mgraph.pack_start(box_content_mgraph, False, False, 0)

        # label = Gtk.Label("Under Contruction")
        stack.add_titled(box_mgraph, 'Measurement Graph', 'Measurement Graph')
        # End Protocol Compare Tab

#=========================================================================================================================================
        # EXCEL TO JSON
#=========================================================================================================================================

        # Excel to Json
        box_excel_to_json = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_content_excel_to_json  = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        box_content_blank = Gtk.Box(spacing=10)
        box_content_blank.set_size_request(1, 15)
        box_content_main_excel_to_json = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_content_excel_to_json.pack_start(box_content_blank, False, False, 0)
        box_content_excel_to_json.pack_start(box_content_main_excel_to_json, False, False, 0)
        box_excel_to_json.pack_start(box_content_excel_to_json, False, False, 0)
        label = Gtk.Label("Under Contruction")
        label.set_margin_top(10)
        box_content_main_excel_to_json.add(label)
        # button 1
        button_excel_to_json = Gtk.Button("Select Excel")
        button_excel_to_json.set_property("width-request", 130)
        button_excel_to_json.connect("clicked", self.excel_to_json_upload)
        # Path 1
        self.path_excel_to_json = Gtk.Entry()
        self.path_excel_to_json.set_property("width-request", 450)
        self.path_excel_to_json.set_text("")

        layout_excel = Gtk.Box(spacing=10)
        layout_excel.set_homogeneous(False)
        vbox_left_excel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_left_excel.set_homogeneous(False)
        vbox_right_excel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right_excel.set_margin_right(10)
        vbox_right_excel.set_homogeneous(False)
        # Make two columns
        layout_excel.pack_start(vbox_left_excel, True, True, 0)
        layout_excel.pack_start(vbox_right_excel, True, True, 0)

        button_excel_to_json.set_margin_top(10)
        self.path_excel_to_json.set_margin_top(10)
        vbox_left_excel.add(button_excel_to_json)
        vbox_right_excel.add(self.path_excel_to_json)
        # label = Gtk.Label("Under Contruction")
        # label.set_margin_top(10)
        # box_content_main_excel_to_json.pack_start(label, False, False, 0)
        box_content_main_excel_to_json.pack_start(layout_excel, False, False, 0)

        layout_last_excel = Gtk.Box(spacing=10)
        layout_last_excel.set_margin_right(10)
        layout_last_excel.set_margin_bottom(5)
        button_last_excel = Gtk.Button("Export")
        button_last_excel.set_margin_end(400)
        button_last_excel.set_margin_top(10)
        button_last_excel.connect("clicked", self.button_excel_json_export)
        label_last_excel = Gtk.Label("")
        label_last_excel.set_property("width-request", 450)
        layout_last_excel.add(label_last_excel)
        # layout_last.add(button_update)
        vbox_right_excel.add(button_last_excel)
        # layout_last.add(button_last)
        box_content_main_excel_to_json.pack_start(layout_last_excel, False, False, 10)



        # box_content_main_excel_to_json.pack_start(label, False, False, 0)
        stack.add_titled(box_excel_to_json, 'Excel to Json', 'Excel to Json')
        # End Excel to Json

        self.path1_config.set_text(author)

# =========================================================================================================================================
        # About
# =========================================================================================================================================

        # About Tab
        about_box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        about_box.set_homogeneous(False)
        about_box.set_border_width(10)
        label = Gtk.Label()
        label.set_text("CorePyTools"
                       "\n____________________________________________________________________"
                       "______________________________________________________________________\n"
                       "\nVersion 1.0.0"
                       "\nDeveloped by lam.chien"
                       "\nPublished on 2 Jan 2019"
                       "\nSupport: Some kind of measurement on (v)MME, (v)GW")
        label.set_justify(Gtk.Justification.LEFT)
        about_box.pack_start(label, False, False, 0)
        stack.add_titled(about_box, 'About', 'About')
        # End About Tab

# =========================================================================================================================================
    # Define function
# =========================================================================================================================================

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

    def button_excel_json_export(self, widget):
        print "Clicked button_excel_json_export"

    def button_config_compare(self, widget):
        print author
        print "Config Compare Final"
        now = datetime.today()
        print 'now: ', now
        first_version = self.first_version_config.get_text()
        print 'first_version: ',first_version
        first_prompt = self.first_prompt_config.get_text()
        print 'first_prompt: ', first_prompt
        second_version = self.second_version_config.get_text()
        print 'second_version: ', second_version
        second_prompt = self.second_prompt.get_text()
        print 'second_prompt: ', second_prompt
        path1 = self.path1_config.get_text()
        print 'path1: ', path1
        path2 = self.path2_config.get_text()
        print 'path2: ', path2
        config = self.path3_config.get_text()
        print 'config: ', config

        print "Show Highchart"
        win = Gtk.Window()
        win.set_default_size(800, 500)
        web = WebKit.WebView()
        # web.open("http://google.com")
        uri = 'web/page.html'
        uri = os.path.realpath(uri)
        uri = urlparse.ParseResult('file', '', uri, '', '', '')
        uri = urlparse.urlunparse(uri)
        web.load_uri(uri)
        web.connect("load-finished", get_source)
        win.add(web)
        win.show_all()


    def button_measurement_compare(self, widget):
        print "Measurement Compare Final"
        now = datetime.today()
        print 'now: ', now
        print 'paramiko:', paramiko.__version__
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

    def excel_to_json_upload(self, widget):
        print "Go to excel_to_json_upload"
        dialog = Gtk.FileChooserDialog("Select a file", self, Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Open", Gtk.ResponseType.OK
                                        )
                                       )
        dialog.set_default_size(800, 400)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print "Open Clicked"
            print ("File: " + dialog.get_filename())
            self.path_excel_to_json.set_text(unicode(dialog.get_filename(), "utf-8"))
            # print ("Path: "+dialog.get_file())
            # fp = open(self.path1.get_text)
            # for line in fp:
            #     print line
        elif response == Gtk.ResponseType.CANCEL:
            print ("Cancel Clicked")
        dialog.destroy()

    def config_compare_upload1(self, widget):
        print "Go to config_compare_upload1"
        dialog = Gtk.FileChooserDialog("Select a file", self, Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Open", Gtk.ResponseType.OK
                                        )
                                       )
        dialog.set_default_size(800, 400)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print "Open Clicked"
            print ("File: " + dialog.get_filename())
            self.path1_config.set_text(unicode(dialog.get_filename(), "utf-8"))
            # print ("Path: "+dialog.get_file())
            # fp = open(self.path1.get_text)
            # for line in fp:
            #     print line
        elif response == Gtk.ResponseType.CANCEL:
            print ("Cancel Clicked")
        dialog.destroy()

    def config_compare_upload2(self, widget):
        print "Go to config_compare_upload2"
        dialog = Gtk.FileChooserDialog("Select a file", self, Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Open", Gtk.ResponseType.OK
                                        )
                                       )
        dialog.set_default_size(800, 400)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print "Open Clicked"
            print ("File: " + dialog.get_filename())
            self.path2_config.set_text(unicode(dialog.get_filename(), "utf-8"))
            # print ("Path: "+dialog.get_file())
            # fp = open(self.path1.get_text)
            # for line in fp:
            #     print line
        elif response == Gtk.ResponseType.CANCEL:
            print ("Cancel Clicked")
        dialog.destroy()

    def config_compare_upload3(self, widget):
        print "Go to config_compare_upload3"
        dialog = Gtk.FileChooserDialog("Select a file", self, Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Open", Gtk.ResponseType.OK
                                        )
                                       )
        dialog.set_default_size(800, 400)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print "Open Clicked"
            print ("File: " + dialog.get_filename())
            self.path3_config.set_text(unicode(dialog.get_filename(), "utf-8"))
            # print ("Path: "+dialog.get_file())
            # fp = open(self.path1.get_text)
            # for line in fp:
            #     print line
        elif response == Gtk.ResponseType.CANCEL:
            print ("Cancel Clicked")
        dialog.destroy()

    def measurement_compare_upload1(self, widget):
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

    def measurement_compare_upload2(self, widget):
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


window = MenuExampleWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()



# # =========================================================================================================================================
#         # Protocol Compare
# # =========================================================================================================================================
#
#         # Protocol Compare Tab
#         box_protocol = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
#         box_content_protocol = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
#         box_content_blank = Gtk.Box(spacing=10)
#         box_content_blank.set_size_request(1, 15)
#         box_content_main_protocol = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
#         box_content_protocol.pack_start(box_content_blank, False, False, 0)
#         box_content_protocol.pack_start(box_content_main_protocol, False, False, 0)
#         label = Gtk.Label("Under Contruction")
#         label.set_margin_top(10)
#         box_content_main_protocol.add(label)
#         box_protocol.pack_start(box_content_protocol, False, False, 0)
#
#         # label = Gtk.Label("Under Contruction")
#         stack.add_titled(box_protocol, 'Protocol Compare', 'Protocol Compare')
#         # End Protocol Compare Tab
