import pandas as pd
import csv

with open('tests_010_010.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    working_instances = 0
    time = 0
    time_limit = 0
    imparity_quotient = 0
    gap = 0
    for row in csv_reader:
        if working_instances == 0:
            print(f'Column names are {", ".join(row)}')
        #print(f'\t{row["Instance"]}')
        working_instances += 1
        if (row["Time"] != '3600.0'):
            time += float(row["Time"])
        else:
            print(f'\t{row["Gap"]}')
            time_limit += 1
            gap += float(row["Gap"])
        imparity_quotient += float(row["Imparity Quotient"])
    working_avg_time = time/working_instances
    avg_time = (time + 3600*(320-working_instances+time_limit))/320
    avg_imparity_quotient = imparity_quotient/working_instances
    avg_gap = gap/time_limit
    print (working_avg_time)
    print (avg_time)
    print (avg_imparity_quotient)
    print (avg_gap)
    print (working_instances)
    print (time_limit)