import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from smbus import SMBus

'''
i2c GUI - change bits at certain addresses
v1.0 
TODOs:
remove methods + add resuability
'''

root = tk.Tk()
bus = SMBus(1)
fontStyle = tkFont.Font(family="Lucida Grande", size=10)

def delete0x00():
    output_blank_0x00.delete(0, 'end')
def read0x00():
	bits = bus.read_byte_data(0x55, 0x00)
	output_blank_0x00.insert(0,bin(bits))
def write0x00():
	bits = bus.read_byte_data(0x55, 0x00)
	entry_val = entry_0x00.get()
	keep = format(int(bits), "b")
	keep = keep[:3]
	final = str(keep) + str(entry_val)
	print(int(final,2))
	bus.write_byte_data(0x55, 0x00, int(final,2))

address_0x00 = tk.Label(root, text="0x00")
description_0x00 = tk.Label(root, text="bandgap",font=fontStyle)
entry_0x00 = tk.Entry(root, width=5)
input_text_0x00 = tk.Label(root, text="5-trimming code",font=fontStyle)
output_text_0x00 = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x00 = tk.Entry(root, width=10)
read_0x00_button = tk.Button(root, text='Read', command=lambda:[delete0x00(), read0x00()])
write_0x00_button = tk.Button(root, text='Write', command=write0x00)

address_0x00.grid(row=0, column=0)
description_0x00.grid(row=0, column=1)
entry_0x00.grid(row=0, column=2)
input_text_0x00.grid(row=1, column=2)
output_text_0x00.grid(row=0, column=6)
output_blank_0x00.grid(row=0, column=7)
read_0x00_button.grid(row=0, column=8)
write_0x00_button.grid(row=0, column=9)


def delete0x01():
    output_blank_0x01.delete(0, 'end')
def read0x01():
	bits = bus.read_byte_data(0x55, 0x01)
	output_blank_0x01.insert(0,bin(bits))
def write0x01():
	#read_byte_data
	bits = bus.read_byte_data(0x55, 0x01)
	entry_val = entry_0x01_47.get()
	entry_val_2 = entry_0x01_02.get()
	keep = format(int(bits), "b")
	keep = keep[4:5]
	final = str(entry_val) + str(keep) + str(entry_val_2)
	print(int(final,2))
	bus.write_byte_data(0x55, 0x01, int(final,2))

address_0x01 = tk.Label(root, text="0x01")
description_0x01 = tk.Label(root, text="TIA ref and bias current",font=fontStyle)
entry_0x01_47 = tk.Entry(root,width=4)
entry_0x01_02 = tk.Entry(root,width=3)
input_text_0x01 = tk.Label(root, text="4-bias control",font=fontStyle)
input_text_0x01_2 = tk.Label(root, text="3-TIA voltage",font=fontStyle)
output_text_0x01 = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x01 = tk.Entry(root, width=10)
read_0x01_button = tk.Button(root, text='Read', command=lambda:[delete0x01(), read0x01()])
write_0x01_button = tk.Button(root, text='Write', command=write0x01)

address_0x01.grid(row=2, column=0)
description_0x01.grid(row=2, column=1)
entry_0x01_47.grid(row=2, column=2)
entry_0x01_02.grid(row=2, column=3)
input_text_0x01.grid(row=3, column=2)
input_text_0x01_2.grid(row=3,column=3)
output_text_0x01.grid(row=2, column=6)
output_blank_0x01.grid(row=2, column=7)
read_0x01_button.grid(row=2, column=8)
write_0x01_button.grid(row=2, column=9)


def delete0x02():
    output_blank_0x02.delete(0, 'end')
def read0x02():
	bits = bus.read_byte_data(0x55, 0x02)
	output_blank_0x02.insert(0,bin(bits))
def write0x02():
	bits = bus.read_byte_data(0x55, 0x02)
	entry_val = entry_0x02_6.get()
	entry_val_2 = entry_0x02_5.get()
	entry_val_3 = entry_0x02_4.get()
	entry_val_4 = entry_0x02_02.get()
	keep = format(int(bits), "b")
	keep = keep[:1]
	keep1 = format(int(bits), "b")
	keep1 = keep1[4:5]
	final = str(keep) + str(entry_val) + str(entry_val_2) + str(entry_val_3) + str(keep1) + str(entry_val_4)
	print(int(final,2))
	bus.write_byte_data(0x55, 0x02, int(final,2))

address_0x02 = tk.Label(root, text="0x02")
description_0x02 = tk.Label(root, text="VDD12 ref",font=fontStyle)
entry_0x02_6 = tk.Entry(root,width=1)
entry_0x02_5 = tk.Entry(root,width=1)
entry_0x02_4 = tk.Entry(root,width=1)
entry_0x02_02 = tk.Entry(root,width=3)
input_text_0x02 = tk.Label(root, text="1-LEDDRV_PD",font=fontStyle)
input_text_0x02_2 = tk.Label(root, text="1-LED PD",font=fontStyle)
input_text_0x02_3 = tk.Label(root, text="1-TIA_PD",font=fontStyle)
input_text_0x02_4 = tk.Label(root, text="3-VDD12 REF",font=fontStyle)
output_text_0x02 = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x02 = tk.Entry(root, width=10)
read_0x02_button = tk.Button(root, text='Read', command=lambda:[delete0x02(), read0x02()])
write_0x02_button = tk.Button(root, text='Write', command=write0x02)

address_0x02.grid(row=4, column=0)
description_0x02.grid(row=4, column=1)
entry_0x02_6.grid(row=4, column=2)
entry_0x02_5.grid(row=4, column=3)
entry_0x02_4.grid(row=4, column=4)
entry_0x02_02.grid(row=4, column=5)
input_text_0x02.grid(row=5, column=2)
input_text_0x02_2.grid(row=5, column=3)
input_text_0x02_3.grid(row=5, column=4)
input_text_0x02_4.grid(row=5, column=5)
output_text_0x02.grid(row=4, column=6)
output_blank_0x02.grid(row=4, column=7)
read_0x02_button.grid(row=4,column=8)
write_0x02_button.grid(row=4, column=9)

def delete0x03():
    output_blank_0x03.delete(0, 'end')
def read0x03():
	bits = bus.read_byte_data(0x55, 0x03)
	output_blank_0x03.insert(0,bin(bits))
def write0x03():
	bits = bus.read_byte_data(0x55, 0x03)
	entry_val = entry_0x03_57.get()
	entry_val_2 = entry_0x03_04.get()
	final = str(entry_val) + str(entry_val_2)
	bus.write_byte_data(0x55, 0x03, int(final,2))

address_0x03 = tk.Label(root, text="0x03")
description_0x03 = tk.Label(root, text="offset cancellation ref",font=fontStyle)
entry_0x03_57 = tk.Entry(root,width=3)
entry_0x03_04 = tk.Entry(root,width=5)
input_text_0x03 = tk.Label(root, text="3-o.c swing",font=fontStyle)
input_text_0x03_2 = tk.Label(root, text="5-o.c ref ctrl",font=fontStyle)
output_text_0x03 = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x03 = tk.Entry(root, width=10)
read_0x03_button = tk.Button(root, text='Read', command=lambda:[delete0x03(), read0x03()])
write_0x03_button = tk.Button(root, text='Write', command=write0x03)

address_0x03.grid(row=6, column=0)
description_0x03.grid(row=6, column=1)
entry_0x03_57.grid(row=6, column=2)
entry_0x03_04.grid(row=6, column=3)
input_text_0x03.grid(row=7, column=2)
input_text_0x03_2.grid(row=7,column=3)
output_text_0x03.grid(row=6, column=6)
output_blank_0x03.grid(row=6, column=7)
read_0x03_button.grid(row=6, column=8)
write_0x03_button.grid(row=6, column=9)

def delete0x04():
    output_blank_0x04.delete(0, 'end')
def read0x04():
	bits = bus.read_byte_data(0x55, 0x04)
	output_blank_0x04.insert(0,bin(bits))
def write0x04():
	bits = bus.read_byte_data(0x55, 0x04)
	entry_val = entry_0x04_3.get()
	entry_val_2 = entry_0x04_02.get()
	keep = format(int(bits), "b")
	keep = keep[:4]
	final = str(keep) + str(entry_val) + str(entry_val_2)
	bus.write_byte_data(0x55, 0x04, int(final,2))

address_0x04 = tk.Label(root, text="0x04")
description_0x04 = tk.Label(root, text="")
entry_0x04_3 = tk.Entry(root,width=1)
entry_0x04_02 = tk.Entry(root,width=3)
input_text_0x04 = tk.Label(root, text="1-freeze",font=fontStyle)
input_text_0x04_2 = tk.Label(root, text="3-o.c gain",font=fontStyle)
output_text_0x04 = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x04 = tk.Entry(root, width=10)
read_0x04_button = tk.Button(root, text='Read', command=lambda:[delete0x04(), read0x04()])
write_0x04_button = tk.Button(root, text='Write', command=write0x04)

address_0x04.grid(row=8, column=0)
description_0x04.grid(row=8, column=1)
entry_0x04_3.grid(row=8, column=2)
entry_0x04_02.grid(row=8, column=3)
input_text_0x04.grid(row=9, column=2)
input_text_0x04_2.grid(row=9,column=3)
output_text_0x04.grid(row=8, column=6)
output_blank_0x04.grid(row=8, column=7)
read_0x04_button.grid(row=8, column=8)
write_0x04_button.grid(row=8, column=9)

def delete0x05():
    output_blank_0x05.delete(0, 'end')
def read0x05():
	bits = bus.read_byte_data(0x55, 0x05)
	output_blank_0x05.insert(0,bin(bits))
def write0x05():
	bits = bus.read_byte_data(0x55, 0x05)
	entry_val = entry_0x05_04.get()
	keep = format(int(bits), "b")
	keep = keep[:3]
	final = str(keep) + str(entry_val)
	bus.write_byte_data(0x55, 0x05, int(final,2))

address_0x05 = tk.Label(root, text="0x05")
description_0x05 = tk.Label(root, text="")
entry_0x05_04 = tk.Entry(root,width=5)
input_text_0x05 = tk.Label(root, text="5-o.c max",font=fontStyle)
output_text_0x05 = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x05 = tk.Entry(root, width=10)
read_0x05_button = tk.Button(root, text='Read', command=lambda:[delete0x05(), read0x05()])

address_0x05.grid(row=10, column=0)
description_0x05.grid(row=10, column=1)
entry_0x05_04.grid(row=10, column=2)
input_text_0x05.grid(row=11, column=2)
output_text_0x05.grid(row=10, column=6)
output_blank_0x05.grid(row=10, column=7)
read_0x05_button.grid(row=10, column=8)

def delete0x06():
    output_blank_0x06.delete(0, 'end')
def read0x06():
	bits = bus.read_byte_data(0x55, 0x06)
	output_blank_0x06.insert(0,bin(bits))
def write0x06():
	bits = bus.read_byte_data(0x55, 0x06)
	entry_val = entry_0x06_04.get()
	keep = format(int(bits), "b")
	keep = keep[:3]
	final = str(keep) + str(entry_val)
	bus.write_byte_data(0x55, 0x06, int(final,2))

address_0x06 = tk.Label(root, text="0x06")
description_0x06 = tk.Label(root, text="")
entry_0x06_04 = tk.Entry(root,width=5)
input_text_0x06 = tk.Label(root, text="5-o.c min",font=fontStyle)
output_text_0x06 = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x06 = tk.Entry(root, width=10)
read_0x06_button = tk.Button(root, text='Read', command=lambda:[delete0x06(), read0x06()])

address_0x06.grid(row=12, column=0)
description_0x06.grid(row=12, column=1)
entry_0x06_04.grid(row=12, column=2)
input_text_0x06.grid(row=13, column=2)
output_text_0x06.grid(row=12, column=6)
output_blank_0x06.grid(row=12, column=7)
read_0x06_button.grid(row=12, column=8)

def delete0x07():
    output_blank_0x07.delete(0, 'end')
def read0x07():
	bits = bus.read_byte_data(0x55, 0x07)
	output_blank_0x07.insert(0,bin(bits))
def write0x07():
	bits = bus.read_byte_data(0x55, 0x07)
	entry_val = entry_0x07_07.get()
	final = str(entry_val)
	bus.write_byte_data(0x55, 0x07, int(final,2))

address_0x07 = tk.Label(root, text="0x07")
description_0x07 = tk.Label(root, text="")
entry_0x07_07 = tk.Entry(root,width=8)
input_text_0x07 = tk.Label(root, text="8-o.c channel monitored",font=fontStyle)
output_text_0x07 = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x07 = tk.Entry(root, width=10)
read_0x07_button = tk.Button(root, text='Read', command=lambda:[delete0x07(), read0x07()])
write_0x07_button = tk.Button(root, text='Write', command=write0x07)

address_0x07.grid(row=14, column=0)
description_0x07.grid(row=14, column=1)
entry_0x07_07.grid(row=14, column=2)
input_text_0x07.grid(row=15, column=2)
output_text_0x07.grid(row=14, column=6)
output_blank_0x07.grid(row=14, column=7)
read_0x07_button.grid(row=14, column=8)
write_0x07_button.grid(row=14, column=9)

def delete0x08():
    output_blank_0x08.delete(0, 'end')
def read0x08():
	bits = bus.read_byte_data(0x55, 0x08)
	output_blank_0x08.insert(0,bin(bits))
def write0x08():
	bits = bus.read_byte_data(0x55, 0x08)
	entry_val = entry_0x08_6.get()
	entry_val_2 = entry_0x08_04.get()
	keep = format(int(bits), "b")
	keep = keep[:1]
	keep1 = format(int(bits), "b")
	keep1 = keep1[2:3]
	final = str(keep) + str(entry_val) + str(keep1) + str(entry_val_2)
	bus.write_byte_data(0x55, 0x08, int(final,2))

address_0x08 = tk.Label(root, text="0x08")
description_0x08 = tk.Label(root, text="")
entry_0x08_6 = tk.Entry(root,width=1)
entry_0x08_04 = tk.Entry(root,width=5)
input_text_0x08 = tk.Label(root, text="1-global lock",font=fontStyle)
input_text_0x08_2 = tk.Label(root, text="5-o.c DAC level",font=fontStyle)
output_text_0x08 = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x08 = tk.Entry(root, width=10)
read_0x08_button = tk.Button(root, text='Read', command=lambda:[delete0x08(), read0x08()])

address_0x08.grid(row=16, column=0)
description_0x08.grid(row=16, column=1)
entry_0x08_6.grid(row=16, column=2)
entry_0x08_04.grid(row=16, column=3)
input_text_0x08.grid(row=17, column=2)
input_text_0x08_2.grid(row=17, column=3)
output_text_0x08.grid(row=16, column=6)
output_blank_0x08.grid(row=16, column=7)
read_0x08_button.grid(row=16, column=8)

def delete0x09():
    output_blank_0x09.delete(0, 'end')
def read0x09():
	bits = bus.read_byte_data(0x55, 0x09)
	output_blank_0x09.insert(0,bin(bits))
def write0x09():
	bits = bus.read_byte_data(0x55, 0x09)
	entry_val = entry_0x09_04.get()
	keep = format(int(bits), "b")
	keep = keep[:3]
	final = str(keep) + str(entry_val)
	bus.write_byte_data(0x55, 0x09, int(final,2))

address_0x09 = tk.Label(root, text="0x09")
description_0x09 = tk.Label(root, text="")
entry_0x09_04 = tk.Entry(root,width=5)
input_text_0x09 = tk.Label(root, text="5-o.c DAC override",font=fontStyle)
output_text_0x09 = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x09 = tk.Entry(root, width=10)
read_0x09_button = tk.Button(root, text='Read', command=lambda:[delete0x09(), read0x09()])
write_0x09_button = tk.Button(root, text='Write', command=write0x09)

address_0x09.grid(row=18, column=0)
description_0x09.grid(row=18, column=1)
entry_0x09_04.grid(row=18, column=2)
input_text_0x09.grid(row=19, column=2)
output_text_0x09.grid(row=18, column=6)
output_blank_0x09.grid(row=18, column=7)
read_0x09_button.grid(row=18, column=8)
write_0x09_button.grid(row=18, column=9)

def delete0x0A():
    output_blank_0x0A.delete(0, 'end')
def read0x0A():
	bits = bus.read_byte_data(0x55, 0x0A)
	output_blank_0x0A.insert(0,bin(bits))
def write0x0A():
	bits = bus.read_byte_data(0x55, 0x0A)
	entry_val = entry_0x0A_04.get()
	keep = format(int(bits), "b")
	keep = keep[:3]
	final = str(keep) + str(entry_val)
	bus.write_byte_data(0x55, 0x0A, int(final,2))

address_0x0A = tk.Label(root, text="0x0A")
description_0x0A = tk.Label(root, text="LED CONTROL",font=fontStyle)
entry_0x0A_04 = tk.Entry(root,width=5)
input_text_0x0A = tk.Label(root, text="5-LED BIAS",font=fontStyle)
output_text_0x0A = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x0A = tk.Entry(root, width=10)
read_0x0A_button = tk.Button(root, text='Read', command=lambda:[delete0x0A(), read0x0A()])
write_0x0A_button = tk.Button(root, text='Write', command=write0x0A)

address_0x0A.grid(row=20, column=0)
description_0x0A.grid(row=20, column=1)
entry_0x0A_04.grid(row=20, column=2)
input_text_0x0A.grid(row=21, column=2)
output_text_0x0A.grid(row=20, column=6)
output_blank_0x0A.grid(row=20, column=7)
read_0x0A_button.grid(row=20, column=8)
write_0x0A_button.grid(row=20, column=9)

def delete0x0B():
    output_blank_0x0B.delete(0, 'end')
def read0x0B():
	bits = bus.read_byte_data(0x55, 0x0B)
	output_blank_0x0B.insert(0,bin(bits))
def write0x0B():
	bits = bus.read_byte_data(0x55, 0x0B)
	entry_val = entry_0x0B_04.get()
	keep = format(int(bits), "b")
	keep = keep[:3]
	final = str(keep) + str(entry_val)
	bus.write_byte_data(0x55, 0x0B, int(final,2))

address_0x0B = tk.Label(root, text="0x0B")
description_0x0B = tk.Label(root, text="")
entry_0x0B_04 = tk.Entry(root,width=5)
input_text_0x0B = tk.Label(root, text="5-LED MOD",font=fontStyle)
output_text_0x0B = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x0B = tk.Entry(root, width=10)
read_0x0B_button = tk.Button(root, text='Read', command=lambda:[delete0x0B(), read0x0B()])
write_0x0B_button = tk.Button(root, text='Write', command=write0x0B)

address_0x0B.grid(row=22, column=0)
description_0x0B.grid(row=22, column=1)
entry_0x0B_04.grid(row=22, column=2)
input_text_0x0B.grid(row=23, column=2)
output_text_0x0B.grid(row=22, column=6)
output_blank_0x0B.grid(row=22, column=7)
read_0x0B_button.grid(row=22, column=8)
write_0x0B_button.grid(row=22, column=9)

def delete0x0C():
    output_blank_0x0C.delete(0, 'end')
def read0x0C():
	bits = bus.read_byte_data(0x55, 0x0C)
	output_blank_0x0C.insert(0,bin(bits))
def write0x0C():
	bits = bus.read_byte_data(0x55, 0x0C)
	entry_val = entry_0x0C_01.get()
	keep = format(int(bits), "b")
	keep = keep[:6]
	final = str(keep) + str(entry_val)
	bus.write_byte_data(0x55, 0x0C, int(final,2))

address_0x0C = tk.Label(root, text="0x0C")
description_0x0C = tk.Label(root, text="")
entry_0x0C_01 = tk.Entry(root,width=2)
input_text_0x0C = tk.Label(root, text="2-LED boost",font=fontStyle)
output_text_0x0C = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x0C = tk.Entry(root, width=10)
read_0x0C_button = tk.Button(root, text='Read', command=lambda:[delete0x0C(), read0x0C()])
write_0x0C_button = tk.Button(root, text='Write', command=write0x0C)

address_0x0C.grid(row=24, column=0)
description_0x0C.grid(row=24, column=1)
entry_0x0C_01.grid(row=24, column=2)
input_text_0x0C.grid(row=25, column=2)
output_text_0x0C.grid(row=24, column=6)
output_blank_0x0C.grid(row=24, column=7)
read_0x0C_button.grid(row=24, column=8)
write_0x0C_button.grid(row=24, column=9)

def delete0x0D():
    output_blank_0x0D.delete(0, 'end')
def read0x0D():
	bits = bus.read_byte_data(0x55, 0x0D)
	output_blank_0x0D.insert(0,bin(bits))
def write0x0D():
	bits = bus.read_byte_data(0x55, 0x0D)
	entry_val = entry_0x0D_04.get()
	keep = format(int(bits), "b")
	keep = keep[:3]
	final = str(keep) + str(entry_val)
	bus.write_byte_data(0x55, 0x0D, int(final,2))

address_0x0D = tk.Label(root, text="0x0D")
description_0x0D = tk.Label(root, text="")
entry_0x0D_04 = tk.Entry(root,width=5)
input_text_0x0D = tk.Label(root, text="5-Input signal reference",font=fontStyle)
output_text_0x0D = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x0D = tk.Entry(root, width=10)
read_0x0D_button = tk.Button(root, text='Read', command=lambda:[delete0x0D(), read0x0D()])
write_0x0D_button = tk.Button(root, text='Write', command=write0x0D)

address_0x0D.grid(row=26, column=0)
description_0x0D.grid(row=26, column=1)
entry_0x0D_04.grid(row=26, column=2)
input_text_0x0D.grid(row=27, column=2)
output_text_0x0D.grid(row=26, column=6)
output_blank_0x0D.grid(row=26, column=7)
read_0x0D_button.grid(row=26, column=8)
write_0x0D_button.grid(row=26, column=9)

def delete0x0E():
    output_blank_0x0E.delete(0, 'end')
def read0x0E():
	bits = bus.read_byte_data(0x55, 0x0E)
	output_blank_0x0E.insert(0,bin(bits))
def write0x0E():
	bits = bus.read_byte_data(0x55, 0x0E)
	entry_val = entry_0x0E_04.get()
	keep = format(int(bits), "b")
	keep = keep[:3]
	final = str(keep) + str(entry_val)
	bus.write_byte_data(0x55, 0x0E, int(final,2))

address_0x0E = tk.Label(root, text="0x0E")
description_0x0E = tk.Label(root, text="")
entry_0x0E_04 = tk.Entry(root,width=5)
input_text_0x0E = tk.Label(root, text="5-Common Mod Ref",font=fontStyle)
output_text_0x0E = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x0E = tk.Entry(root, width=10)
read_0x0E_button = tk.Button(root, text='Read', command=lambda:[delete0x0E(), read0x0E()])
write_0x0E_button = tk.Button(root, text='Write', command=write0x0E)

address_0x0E.grid(row=28, column=0)
description_0x0E.grid(row=28, column=1)
entry_0x0E_04.grid(row=28, column=2)
input_text_0x0E.grid(row=29, column=2)
output_text_0x0E.grid(row=28, column=6)
output_blank_0x0E.grid(row=28, column=7)
read_0x0E_button.grid(row=28, column=8)
write_0x0E_button.grid(row=28, column=9)

def delete0x0F():
    output_blank_0x0F.delete(0, 'end')
def read0x0F():
	bits = bus.read_byte_data(0x55, 0x0F)
	output_blank_0x0F.insert(0,bin(bits))
def write0x0F():
	bits = bus.read_byte_data(0x55, 0x0F)
	entry_val = entry_0x0F_76.get()
	entry_val_2 = entry_0x0F_53.get()
	entry_val_3 = entry_0x0F_21.get()
	entry_val_4 = entry_0x0F_0.get()
	final = str(entry_val) + str(entry_val_2) + str(entry_val_3) + str(entry_val_4)
	bus.write_byte_data(0x55, 0x0F, int(final,2))

address_0x0F = tk.Label(root, text="0x0F")
description_0x0F = tk.Label(root, text="")
entry_0x0F_76 = tk.Entry(root,width=2)
entry_0x0F_53 = tk.Entry(root,width=3)
entry_0x0F_21 = tk.Entry(root,width=2)
entry_0x0F_0 = tk.Entry(root,width=1)
input_text_0x0F = tk.Label(root, text="2-spare bits",font=fontStyle)
input_text_0x0F_2 = tk.Label(root, text="3-test_mux8",font=fontStyle)
input_text_0x0F_22 = tk.Label(root, text="\n0-nothing\n1-REFH\n2-REFL\n3-compref\n4-VDD12ref\n5-DAC1INN\n6-DACINP\n7-VOCMFP",font=fontStyle)
input_text_0x0F_3 = tk.Label(root, text="2-test_mux",font=fontStyle)
input_text_0x0F_33 = tk.Label(root, text="\n0-TIA REF\n1-VBIAS18",font=fontStyle)
input_text_0x0F_4 = tk.Label(root, text="1-Protect LED driver",font=fontStyle)
output_text_0x0F = tk.Label(root, text="output: ",font=fontStyle)
output_blank_0x0F = tk.Entry(root, width=10)
read_0x0F_button = tk.Button(root, text='Read', command=lambda:[delete0x0F(), read0x0F()])
write_0x0F_button = tk.Button(root, text='Write', command=write0x0F)

address_0x0F.grid(row=30, column=0)
description_0x0F.grid(row=30, column=1)
entry_0x0F_76.grid(row=30, column=2)
entry_0x0F_53.grid(row=30, column=3)
entry_0x0F_21.grid(row=30, column=4)
entry_0x0F_0.grid(row=30, column=5)
input_text_0x0F.grid(row=31, column=2)
input_text_0x0F_2.grid(row=31, column=3)
input_text_0x0F_3.grid(row=31, column=4)
input_text_0x0F_22.grid(row=32, column=3)
input_text_0x0F_33.grid(row=32, column=4)
input_text_0x0F_4.grid(row=31, column=5)
output_text_0x0F.grid(row=30, column=6)
output_blank_0x0F.grid(row=30, column=7)
read_0x0F_button.grid(row=30, column=8)
write_0x0F_button.grid(row=30, column=9)


root.mainloop()

