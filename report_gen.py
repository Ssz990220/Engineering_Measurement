import csv

f = open('report.csv','w',encoding = 'utf-8',newline='')

csv_writer = csv.writer(f)
csv_writer.writerow(['a','b','e','f','d','alpha'])

f.close()
