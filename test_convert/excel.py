
import json
import xlsxwriter
with open('config.json', 'r') as f:
    config = json.load(f)
name = config['file_export']

print config['data']['file2'][0]
workbook = xlsxwriter.Workbook(name+'.xlsx')
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


