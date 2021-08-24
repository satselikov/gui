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
comport = 'COM6'
ser = serial.Serial(comport)

#thorlbas
import visa
from ThorlabsPM100 import ThorlabsPM100
rm = visa.ResourceManager()
#inst = rm.open_resource('USB0::0x1313::0x8078::P0024799::INSTR') for PM100D
inst = rm.open_resource('USB0::0x1313::0x8072::P2005317::INSTR')  #for PM100USB

print(inst)
power_meter = ThorlabsPM100(inst=inst)
#power_meter.sense.average.count =100
test_pow = power_meter.read
print(test_pow)


J_min = input("Minimum current density A/cm^2:")
exp_min = int(math.log10(J_min))
J_max = input("Maximum current density A/cm^2:")
exp_max = int(math.log10(J_max))
#Num_points = input("Number of Points:")
Num_points = 10
uLED_size = input("uLED_size um:")
array = input("Is it array? 1 or 0:")
#max_ave = input("Num_averages_for Detector:")
max_ave = 10
wafer_id = input("Enter WaferID: ")
date = input("Enter Date: ")

x_col = input("Enter X/Column: ")
y_row = input("Enter Y/Row: ")
leftright = input("Left or Right: ")
which_col = input("Which column?: ")

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
#output file:
import pandas as pd
import tkinter as tkinter
from tkinter import filedialog
from tkFileDialog import asksaveasfile
from tkinter import filedialog as fd
from tkinter import *
#import Workbook 
import  xlsxwriter 
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

current_array = []
voltage_array = []
power_array = []
J_array = []
QE_array = []
m=1
for each in range(exp_min,exp_max): #length of array
	for each1 in range(1,Num_points):
	   # time.sleep(1)
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
		time.sleep(0.1)
	#measure voltage
		addr_dmm = '22'
		ser.write("++addr"+addr_dmm+"\n")
		ser.write("++auto 1\n")
		ser.write("++eos 3\n")
		ser.write("++eoi 1\n")
		ser.write("MEAS:VOLT:DC? 10,0.003"+"\n")
		v = float(ser.readline())
		voltage_array.append(v)
		time.sleep(0.1)
		pow = 0
		k=0
		for k in range(max_ave):
			pow = pow + power_meter.read
#			print(k)
		power_array.append(pow/max_ave)
		QE_array.append(pow/(max_ave*current_to_set))
		print(pow/max_ave)
		print(curr_buff)

curr_buff = "%f" % 0
addr_yoko = '1'
ser.write("++addr"+addr_yoko+"\n") #address
ser.write("++auto 0\n")
ser.write("++eos 3\n")
ser.write("++eoi 1\n")
ser.write("S"+curr_buff+"\n")
ser.write("O0"+"\n")
ser.write("E"+"\n")

#print(voltage_array)
#print (current_array)
#print (power_array)
LI_curve = {'Current': current_array, 'Voltage': voltage_array, 'Power': power_array, 'Current Density': J_array,'QE': QE_array}


##############################################################
import jsonpickle
import json
import pymongo
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import *


my_dict = {}
my_dict["voltage"] = voltage_array
my_dict["current"] = current_array
my_dict["power"] = power_array
my_dict["current_density"] = J_array
my_dict["quantum efficiency"] = QE_array


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
            'Col' : which_col,
        }]
}

meta_data.update(my_dict)

json_res = jsonpickle.encode(meta_data)
pretty_json = json.dumps(json.loads(json_res), indent=4)#, sort_keys=True)
# print(pretty_json)
with open('E://test_script//test.json', 'w') as json_file: #change file location
    json_file.write(pretty_json)

#client = pymongo.MongoClient('localhost', 27017)
client = pymongo.MongoClient('mongodb://useradmin:avicenatech@167.172.220.133:27017')
db = client['Database']
collection_name = 'LIV'
db_cm = db[collection_name]
with open('E://test_script//test.json', "r") as data_file: #change file location
    data_json = json.load(data_file)

db_cm.insert_one(data_json)



##############################################################


print("open output file....")
root = Tk()
path_excel = filedialog.asksaveasfile(mode="w", defaultextension=".xlsx")
df = pd.DataFrame(LI_curve,columns = ['Current','Voltage','Power', 'Current Density','QE'])
df.to_excel(excel_writer = path_excel.name)
 

#HP stuff
#addr_hp = '16'
#ser.write("++addr"+addr_hp+"\n") #address
#ser.write("++auto 1\n")
#ser.write("++eos 3\n")
#ser.write("++eoi 0\n")
#ser.write("FORM4;OUTPFORM;\n")

#s21_array=[]

#line = ser.readline()
#print(line)
#line = ser.readline()
#print(line)
#line = ser.readline()
#print(line)
#line = ser.readline()
#print(line)
#line = ser.readline()
#print(line)
#line = ser.readline()
#print(line)
#s21_array.append(line)
#k = 1
#while k < 800:
#	print(line)
#	line = ser.readline()
#	split_list = line.split(', ')
#	print(split_list[0])
#	s21_array.append(split_list[0])
#	k = k+1

#print(s21_array)

