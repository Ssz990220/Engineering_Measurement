import csv

f = open('report.csv','a+',encoding = 'utf-8',newline='')

csv_writer = csv.writer(f)
for i in range(0,10):
    csv_writer.writerow([1,2,3,4,5,6])