# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Calculate volume for each 20-minute time window.
"""
import math
from datetime import datetime,timedelta

#cd /Users/apple/code_tool/KDD_run/KDD_python
#python volume_vehicle_model.py
#要改3个地方（out_suffix、fw.writelines、in_file）

file_suffix = '.csv'
path = '/Users/apple/code_tool/KDD_run/KDD_r/volume/vehicle_type|has_etc/'   # set the data directory（改文件路径）

def avgVolume(in_file):

    out_suffix = '_split_vehicle_typeNa'        #---
    in_file_name = in_file + file_suffix
    out_file_name = in_file.split('_')[1] + out_suffix + file_suffix

    # Step 1: Load volume data
    fr = open(path + in_file_name, 'r')
    fr.readline()  # skip the header
    vol_data = fr.readlines()
    fr.close()

    # Step 2: Create a dictionary to caculate and store volume per time window
    volumes = {}  # key: time window value: dictionary
    for i in range(len(vol_data)):
        each_pass = vol_data[i].replace('"', '').split(',')
        tollgate_id = each_pass[1]
        direction = each_pass[2]

        pass_time = each_pass[0]
        pass_time = datetime.strptime(pass_time, "%Y-%m-%d %H:%M:%S")
        time_window_minute = int(math.floor(pass_time.minute / 20) * 20)
        #print pass_time
        start_time_window = datetime(pass_time.year, pass_time.month, pass_time.day,
                                     pass_time.hour, time_window_minute, 0)

        if start_time_window not in volumes:
            volumes[start_time_window] = {}
        if tollgate_id not in volumes[start_time_window]:
            volumes[start_time_window][tollgate_id] = {}
        if direction not in volumes[start_time_window][tollgate_id]:
            volumes[start_time_window][tollgate_id][direction] = 1
        else:
            volumes[start_time_window][tollgate_id][direction] += 1
        #计算那个时刻-那个收费站-那个方向的车辆总数

    # Step 3: format output for tollgate and direction per time window
    fw = open(out_file_name, 'w')
    fw.writelines(','.join(['"tollgate_id"', '"time_window"', '"direction"', '"vehicle_typeNa"',  #---
                            '"start_month"', '"start_day"','"start_hour"', '"start_minute"']) + '\n')
    time_windows = list(volumes.keys())
    time_windows.sort()
    for time_window_start in time_windows:
        time_window_end = time_window_start + timedelta(minutes=20)
        for tollgate_id in volumes[time_window_start]:
            for direction in volumes[time_window_start][tollgate_id]:
               out_line = ','.join(['"' + str(tollgate_id) + '"', 
			                     '"[' + str(time_window_start) + ',' + str(time_window_end) + ')"',
                                 '"' + str(direction) + '"',
                                 '"' + str(volumes[time_window_start][tollgate_id][direction]) + '"',
                                    '"' + str(time_window_start.month) + '"',
                                    '"' + str(time_window_start.day) + '"',
                                    '"' + str(time_window_start.hour) + '"',
                                    '"' + str(time_window_start.minute) + '"'
                                    ]) + '\n'
               fw.writelines(out_line)
    fw.close()

def main():

    in_file = 'volume_vehicle_typeNa_training'    #-------随着车型每次改变
    avgVolume(in_file)

if __name__ == '__main__':
    main()


