import csv

# with open('paris_metro_lines.csv') as file:
#     a = csv.reader(file)
#     for line in a:
#         b = line[0]
#         c = b.replace(' ', ',')
#         print(c)d

with open('paris_metro_lines.csv') as file:
    a = csv.reader(file)
    new_data = []
    for row in a:
        new_data.append([int(row[0]), int(row[1]), int(float(row[2]))])

with open('paris_metro_lines.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(new_data)
