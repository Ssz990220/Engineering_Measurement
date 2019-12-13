import csv
import numpy as np

def gen_report(list):
    f = open('report.csv','a+',encoding='utf-8',newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(list)

if __name__ =='__main__':
    gen_report([2,3,4,5,6,7])




