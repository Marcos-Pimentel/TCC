import pandas as pd
import csv
from os import walk
import math

path='Tables/tests_010_010/'

files = next(walk(path), (None, None, []))[2]

row_list = list()
for file in files:
    if file != 'table.csv':
        with open(path+file, mode='r') as csv_file:
            csv_reader = list(csv.DictReader(csv_file))
            working_instances = 0
            time = 0
            time_limit = 0
            deadhead = 0
            gap = 0
            for row in csv_reader:
                time+=float(row['Time'])
                deadhead+=float(row['Deadhead'])
                gap+=float(row['Gap'])
                working_instances+=1
                if row['Time'] == '3600.0':
                    time_limit+=1
            
            time_total = (20-working_instances)*3600.0+time
            time_avg = time_total/20
            
            if working_instances > 0:
                deadhead_avg = deadhead/working_instances
                gap_avg = gap/working_instances
                deadhead = 0
                gap = 0
                for row in csv_reader:
                    deadhead+=pow(float(row['Deadhead'])-deadhead_avg,2)
                    gap+=pow(float(row['Gap'])-gap_avg,2)
                deadhead_sd = math.sqrt(deadhead/working_instances)
                gap_sd = math.sqrt(gap/working_instances)
            else:
                deadhead_avg = 'Inf'
                deadhead_sd = 'Inf'
                gap_avg = 'Inf'
                gap_sd = 'Inf'
            
            time = 0
            for row in csv_reader:
                time+=pow(float(row['Time'])-time_avg,2)
            time_sd = math.sqrt(time/20)
            
            
            working_percentage = working_instances*5
            optimal_percentage = (working_instances-time_limit)*5
            
            
            
            time_avg=round(time_avg,1)
            time_sd=round(time_sd,1)
            if working_instances > 0:
                gap_avg *= 100
                gap_avg=round(gap_avg,1)
                gap_sd=round(gap_sd,1)
                deadhead_avg=round(deadhead_avg,1)
                deadhead_sd=round(deadhead_sd,1)
            working_percentage=round(working_percentage,1)
            optimal_percentage=round(optimal_percentage,1)
            
            
            row_list.append({
                'Instance Group':file,
                'time':str(time_avg)+' += '+str(time_sd),
                'GAP':str(gap_avg)+' += '+str(gap_sd),
                'working':working_percentage,
                'optimal':optimal_percentage,
                'deadhead': str(deadhead_avg)+' += '+str(deadhead_sd)
                })
        
df = pd.DataFrame(row_list)
df.to_csv(path+"table.csv", index=False)
        # working_instances = 0
        # time = 0
        # time_limit = 0
        # imparity_quotient = 0
        # gap = 0
        # for row in csv_reader:
        #     if working_instances == 0:
        #         print(f'Column names are {", ".join(row)}')
        #     #print(f'\t{row["Instance"]}')
        #     working_instances += 1
        #     if (row["Time"] != '3600.0'):
        #         time += float(row["Time"])
        #     else:
        #         print(f'\t{row["Gap"]}')
        #         time_limit += 1
        #         gap += float(row["Gap"])
        #     imparity_quotient += float(row["Imparity Quotient"])
        # working_avg_time = time/working_instances
        # avg_time = (time + 3600*(320-working_instances+time_limit))/320
        # avg_imparity_quotient = imparity_quotient/working_instances
        # avg_gap = gap/time_limit
        # print("working avg time:")
        # print (working_avg_time)
        # print("avg time:")
        # print (avg_time)
        # print("avg imparity quotient:")
        # print (avg_imparity_quotient)
        # print("avg gap:")
        # print (avg_gap)
        # print("working instances:")
        # print (working_instances)
        # print("time limit:")
        # print (time_limit)