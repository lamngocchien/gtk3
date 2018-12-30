
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# inherit from Gtk.Window
class MainWindow(Gtk.Window):

    # for the constructor we call the constructor of the super class (and set window title)
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")

        # create button, connect its "clicked" signal to a function, and add it to the window
        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.button_clicked)
        self.add(self.button)
        self.set_size_request(300, 100)

    # make sure to pass in widget, wont work if you dont (more about widgets later)
    def button_clicked(self, widget):
        print("Gametime")

        import json
        import xlsxwriter
        with open('config.json', 'r') as f:
            config = json.load(f)
        name = config['file_export']
        path = 'Export/'
        print config['data']['file2'][0]
        workbook = xlsxwriter.Workbook(path+ name + '.xlsx')
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

        # import json
        #
        # config = {'key1': 'value1', 'key2': [1,2,3,"122222"]}
        #
        # with open('config2.json', 'w') as f:
        #     json.dump(config, f)


# create an instance of that class

window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
