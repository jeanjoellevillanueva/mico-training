#multiplcation table
number = int(input("Enter a number: "))
for i in range(1, 11):
    print(f"{number} x {i} = {number * i}")
########################

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekends = ['Saturday', 'Sunday']
for day in days:
    if day in weekends:
        continue
    print(f"Workdays: {day}")
##################################

file_list = [
    'report.csv',
    'data.xlsx',
    'summary.docx',
    'report.csv',
    'data.csv',
    'data.xlsx'
]
for file in file_list:
    if file_list.count(file) > 1:
        print(f"Duplicate found: {file}")
        break
else:
    print('All files are unique')
###############

i = 1
while i < 4:
    print(i)
    i += 1