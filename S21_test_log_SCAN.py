#intitialize
import numpy as np
import sys
import math
import csv
import time
#pyvisa
import pyvisa
import sys
import usb.core
import usb.util
import usb.backend.libusb1
backend = usb.backend.libusb1.get_backend(find_library=lambda x: "c:\\WINDOWS\\system32\\")
dev = usb.core.find(backend=backend, find_all=True)
from pyvisa import util

#serial
import serial
import sys

#thorlbas
import visa
#from ThorlabsPM100 import ThorlabsPM100
import pandas as pd
import tkinter as tkinter
from tkinter import filedialog
from tkFileDialog import asksaveasfile
from tkinter import filedialog as fd
from tkinter import *
#import Workbook 
import  xlsxwriter 


comport = 'COM6'
ser = serial.Serial(comport)

#rm = visa.ResourceManager()
#inst = rm.open_resource('USB0::0x1313::0x8078::P0024799::INSTR')
#power_meter = ThorlabsPM100(inst=inst)
#power_meter.sense.average.count =100
J_min = input("Minimum current density A/cm^2: ")
exp_min = int(math.log10(J_min))
J_max = input("Maximum current density A/cm^2: ")
exp_max = int(math.log10(J_max))
#Num_points = input("Number of Points: ")
Num_points = 10
print("MetaData Details...")
uLED_size = input("uLED_size um: ")
array = input("Is it array? 1 or 0: ")
wafer_id = input("Enter WaferID: ")
date = input("Enter Date: ")

#Location
x_col = input("Enter X/Column: ")
y_row = input("Enter Y/Row: ")
leftright = input("Left or Right? (L/R): ")
which_col = input("Enter Column: ")

#max_ave = input("Num_averages_for Detector:")

#check array size and set multiplication number
if (uLED_size == 2):
	num_uLeds = 100
elif (uLED_size == 4):
	num_uLeds = 25
elif (uLED_size == 8):
	num_uLeds = 9
else:
	num_uLeds = 1
#check if it is an array
if (array == 1):
	I_min = J_min * uLED_size * uLED_size * 1e-8 * num_uLeds
	I_max = J_max * uLED_size * uLED_size * 1e-8 * num_uLeds
else:
	num_uLeds = 1
	I_min = J_min * uLED_size * uLED_size * 1e-8
	I_max = J_max * uLED_size * uLED_size * 1e-8

print(I_min)
print(I_max)

#file_name = raw_input("filename:")
#curr_step = (I_max -I_min)/Num_points

#setup gpib_contorller of Yokogawa
ser.write("++mode 1\n")
addr_yoko = '1'
ser.write("++addr"+addr_yoko+"\n") #address
ser.write("++auto 0\n")     #just talk
ser.write("++eos 3\n")
ser.write("++eoi 1\n")

#turn on current source
time.sleep(0.1)
ser.write("F5"+"\n") #current mode
time.sleep(0.1)
if (I_max > 10e-3):
	ser.write("R6"+"\n") #range is 100mA
	time.sleep(0.1)
elif (I_max > 1e-3):
	ser.write("R5"+"\n") #range is 10mA
	time.sleep(0.1)
else:
	ser.write("R4"+"\n") #range is 1mA
	time.sleep(0.1)
ser.write("O1"+"\n")  #enable the source
time.sleep(0.1)
ser.write("E"+"\n")
curr_buff = "%f" % I_min   #format to string
ser.write("S"+curr_buff+"\n") 
ser.write("E"+"\n")
current_to_set = I_min
N_dp = 402
current_array = []
J_array = []
f_min = input("min frequency  [GHz]:")
f_max = input("max frequency  [GHz]:")

frequency_array = []
f_step = (f_max-f_min)/N_dp
col = ['Frequency']

k=1
f = f_min
while k < N_dp:
	f_buff = "%.10f" % (f*1e9)
	frequency_array.append(f_buff)
	k = k+1
	f = f+ f_step

S21_curve = {'Frequency': frequency_array}

m=1
for each in range(exp_min,exp_max): #length of array
	for each1 in range(1,Num_points):
		#print("start of loop")
		time.sleep(1)
		#set current
		addr_yoko = '1'
		ser.write("++addr"+addr_yoko+"\n") #address
		ser.write("++auto 0\n")
		ser.write("++eos 3\n")
		ser.write("++eoi 1\n")
		curr_dens = each1*math.pow(10,each)
		current_to_set = curr_dens*uLED_size * uLED_size * 1e-8 * num_uLeds
		curr_buff = "%.10f" % current_to_set
		ser.write("S"+curr_buff+"\n")
		time.sleep(0.1)
		ser.write("E"+"\n")
		current_array.append(current_to_set)
		J_array.append(current_to_set/(uLED_size * uLED_size * 1e-8 * num_uLeds))
		j = current_to_set/(uLED_size * uLED_size * 1e-8 * num_uLeds)
		j_buff = "%.10f" % j
		print(j_buff)
		#print("start_sleeping")
		time.sleep(1)#wait for the trace to complete
		#print("end_sleeping")
	#Store the data
	#HP stuff
		addr_hp = '16'
		ser.write("++addr"+addr_hp+"\n") #address
		ser.write("++auto 1\n")
		#ser.write("++eos 3\n")
		ser.write("++eoi 0\n")
#		print("query done")		#line = ser.readline()
		#s21_array.append(line)
#		time.sleep(1)
		ser.write("OPC?;SING\n")# place HP in single sweep mode
		#time.sleep(1)
		rdy = ser.readline() #  read 1 when ready
		print(rdy)
		if(int(rdy) == 1):
			k = 1
			f = f_min
			s21_array = []
#			print("start pulling data")
			time.sleep(1)
			ser.write("FORM4;OUTPFORM;\n") #query the instrument
			while k < (N_dp):
				line = ser.readline()
				split_list = line.split(', ')
				#print(split_list[0])
				s21_array.append(split_list[0])
				k = k+1
				#print(s21_array)
				#print(frequency_array)
			S21_curve[j_buff] = s21_array
			#print(len(s21_array))
			col.append(j_buff)
			print("data_pulled")
		else:
			print("not ready")
#print(S21_curve)

##############################################################
import jsonpickle
import json
import pymongo
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import *

# wafer_id = input("Enter WaferID: ")
# date = input("Enter Date: ")
# size = input("Enter size: ")
# Array = input("Enter Array 1 or 0: ") 


meta_data = {
    'MetaData': 
        [ {
            'WaferID': wafer_id, 
            'Size' : uLED_size,
            'Array' : array,
            'Date' : date,
			'X' : x_col,
            'Y' : y_row,
            'LR' : leftright,
            'Col' : which_col
        }]
}

meta_data.update(S21_curve)

output_dict = {}

for key, value in meta_data.items():
    if key == 'Frequency':
        output_dict[str(key)] = [float(item) for item in value]
    elif key == 'MetaData': 
        output_dict[(key)] = [(item) for item in value]
    else:
        output_dict[int(float(key))] = [float(item) for item in value]
#print("outputdict ", output_dict)


json_res = jsonpickle.encode(output_dict)
pretty_json = json.dumps(json.loads(json_res), indent=4, sort_keys=True)
# print(pretty_json)
with open('E://test_script//TEST_S21_FINAL//test.json', 'w') as json_file: #replace with json file location
    json_file.write(pretty_json)

#client = pymongo.MongoClient('localhost', 27017)
client = pymongo.MongoClient('mongodb://useradmin:avicenatech@167.172.220.133:27017')
db = client['Database']
collection_name = 'S21'
db_cm = db[collection_name]
with open('E://test_script//TEST_S21_FINAL//test.json', "r") as data_file: #replace with json file location
    data_json = json.load(data_file)

db_cm.insert_one(data_json)

##############################################################

#Store the S21 data
print("open S21 output file....")
root = Tk()
path_excel_s21 = filedialog.asksaveasfile(mode="w", defaultextension=".xlsx")
#print(col)
#print(len(S21_curve))
#print(len(col))
df_S21 = pd.DataFrame(S21_curve,columns=col)
df_S21.to_excel(excel_writer = path_excel_s21.name)
	
#turn off current driver
curr_buff = "%f" % 0
addr_yoko = '1'
ser.write("++addr"+addr_yoko+"\n") #address
ser.write("++auto 0\n")
ser.write("++eos 3\n")
ser.write("++eoi 1\n")
ser.write("S"+curr_buff+"\n")
ser.write("O0"+"\n")
ser.write("E"+"\n")
	



