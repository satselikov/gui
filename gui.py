import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import smbus

bus = smbus.SMBus(1)

def init():
    bus.write_byte_data(0x74, 0x06, 0x00)
    bus.write_byte_data(0x74, 0x07, 0x00)
    bus.write_byte_data(0x74, 0x02, 0x00)
    bus.write_byte_data(0x74, 0x03, 0x0c)
    bus.write_byte_data(0x74, 0x03, 0x1c)
    bus.write_i2c_block_data(0x11, 0x05, [0x00, 0xff])
    bus.write_i2c_block_data(0x11, 0x0b, [0x02, 0x00])
    bus.write_i2c_block_data(0x11, 0x03, [0x00, 0x10])
    
root = tk.Tk()
fontStyle = tkFont.Font(family="Lucida Grande", size=17)

def init_labels():
    main_label_dict = {}
    words = ["Voltage", "Current", "Status"]
    for index, val in enumerate(words):
        main_label_dict[val] = tk.Label(root, text=val,
            font=fontStyle).grid(row=0, column=index+1)

    label_dict = {}
    words = ["TIA", "LED", "DRV", "LA", "BF", "BG", "PD",
             "V2_5", "V1_8", "V1_2"]
    for index, val in enumerate(words):
        label_dict[val] = tk.Label(root, text=val,
            font=fontStyle).grid(row = index+1, column = 0)
        
def print_lines():
    print("------------------------")

status = False
def isClicked(button, text, component, bitsON, bitsOFF):
    global status
    status = not status
    print_lines()
    if status:
        button["text"] = "OFF"
        component.set_status(False)
        bus.write_byte_data(0x74, 0x02, bitsOFF)
        print(text + " is disabled.")
        #print(text + " status is" , component.get_status())
    else:
        button["text"] = "ON"
        component.set_status(True)
        bus.write_byte_data(0x74, 0x02, bitsON)
        print(text + " is enabled.")
        #print(text + " status is" , component.get_status())

'''
TODOs:
add offset, slope to variable of power supply object instance
calibrate -> populates offset and slope variable

voltage_entry per component uses slope and offset to set DAC via submit function depending on which component it is
(need to modify submit parameters and pass the correct bits)

somehow save offset + slope per instance and load them up from a file (save + load button add to bottom)
'''

class PowerSupply:
    def __init__(self, voltage, status, slope, offset):
        self.voltage = voltage
        self.status = status
        self.slope = slope
        self.offset = offset 
    def set_voltage(self, voltage):
        self.voltage = voltage
    def get_voltage(self):
        return self.voltage
    def set_status(self, status):
        self.status = status
    def get_status(self):
        return self.status
    def get_slope(self):
        return self.slope
    def set_slope(self, slope):
        self.slope = slope
    def get_offset(self):
        return self.offset
    def set_offset(self, offset):
        self.offset = offset
    
def submit(component, entry, text):
    print_lines()
    print("Clicked submit for: ", text)
    if(len(entry.get()) == 0 ):
        print("Entry for", text, " : None")
    else:
        component.set_voltage(entry.get())
        print("Entry for", text, " :",  entry.get())
    print("Status: ", component.get_status())
    print("Slope: ", component.get_slope())
    print("Offset: ", component.get_offset())


def calibrate(text, a, b, c, b1, c1, component):
    print_lines()
    print("Please Remove ASIC")
    print("SETTING" , text, "TO 0x0000")
    bus.write_i2c_block_data(0x11, a, [b, c])
    print("Please measure value for:", text)
    min_value = float(input("Min Value: "))
    
    print_lines()
    print("SETTING" , text, "TO 0x0FFF")
    bus.write_i2c_block_data(0x11, a, [b1, c1])
    print("Please measure value for:", text)
    max_value = float(input("Max Value: "))
    
    slope = 4096/(max_value - min_value)
    offset = -abs(slope)*min_value
    
    component.set_slope(slope)
    component.set_offset(offset)
    
    print("Slope: ", slope)
    print("Offset: ", offset)
    

# INIT TIA
TIA = PowerSupply(1.8,False,0,0)
TIA_text = "TIA"
button_TIA = tk.Button(root, text="OFF", font=fontStyle,
                       command=lambda:isClicked(button_TIA, TIA_text, TIA, 0x01, 0x00))
button_TIA.grid(row=1, column=3)

TIA_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
TIA_voltage_entry.grid(row=1, column=1)

TIA_submit = tk.Button(root, text="Submit", font=fontStyle,
                       command=lambda:submit(TIA, TIA_voltage_entry, TIA_text))
TIA_submit.grid(row=1,column=4)

TIA_calibrate = tk.Button(root, text="Cal", font=fontStyle,
                          command = lambda:calibrate(TIA_text, 0x10, 0x80, 0x00, 0x8f, 0xff, TIA))
TIA_calibrate.grid(row=1, column=5)
        

# INIT LED
LED = PowerSupply(4.4,False,0,0)
LED_text = "LED"
button_LED = tk.Button(root, text="OFF", font=fontStyle,
                       command=lambda:isClicked(button_LED, LED_text, LED, 0x02, 0x00))
button_LED.grid(row=2, column=3)
    
LED_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
LED_voltage_entry.grid(row=2, column=1)
    
LED_submit = tk.Button(root, text="Submit", font=fontStyle,
                       command=lambda:submit(LED, LED_voltage_entry, LED_text))
LED_submit.grid(row=2,column=4)

# LED_calibrate = tk.Button(root, text="Cal", font=fontStyle,
#                           command = lambda:calibrate(LED_text, 0x10, 0x80, 0x00, 0x8f, 0xff, LED))
# LED_calibrate.grid(row=2, column=5)

# INIT DRV
DRV = PowerSupply(1.0,False,0,0)
DRV_text = "DRV"
button_DRV = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_DRV, DRV_text, DRV, 0x04, 0x00))
button_DRV.grid(row=3, column=3)
    
DRV_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
DRV_voltage_entry.grid(row=3, column=1)
    
DRV_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(DRV, DRV_voltage_entry, DRV_text))
DRV_submit.grid(row=3,column=4)

DRV_calibrate = tk.Button(root, text="Cal", font=fontStyle,
                          command = lambda:calibrate(DRV_text, 0x11, 0x90, 0x00, 0x9f, 0xff, DRV))
DRV_calibrate.grid(row=3, column=5)

# INIT LA
LA = PowerSupply(1.0, False,0,0)
LA_text = "LA"
button_LA = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_LA, LA_text, LA, 0x08, 0x00))
button_LA.grid(row=4, column=3)
    
LA_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
LA_voltage_entry.grid(row=4, column=1)
    
LA_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(LA, LA_voltage_entry, LA_text))
LA_submit.grid(row=4,column=4)

LA_calibrate = tk.Button(root, text="Cal", font=fontStyle,
                          command = lambda:calibrate(LA_text, 0x12, 0xa0, 0x00, 0xaf, 0xff, LA))
LA_calibrate.grid(row=4, column=5)

# INIT BF
BF = PowerSupply(1.0, False,0,0)
BF_text = "BF"
button_BF = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_BF, BF_text, BF, 0x10, 0x00))
button_BF.grid(row=5, column=3)
    
BF_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
BF_voltage_entry.grid(row=5, column=1)
    
BF_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(BF, BF_voltage_entry, BF_text))
BF_submit.grid(row=5,column=4)

BF_calibrate = tk.Button(root, text="Cal", font=fontStyle,
                          command = lambda:calibrate(BF_text, 0x13, 0xb0, 0x00, 0xbf, 0xff, BF))
BF_calibrate.grid(row=5, column=5)
    
# INIT BG
BG = PowerSupply(1.8, False,0,0)
BG_text = "BG"
button_BG = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_BG, BG_text, BG, 0x20, 0x00))
button_BG.grid(row=6, column=3)
    
BG_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
BG_voltage_entry.grid(row=6, column=1)
    
BG_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(BG, BG_voltage_entry, BG_text))
BG_submit.grid(row=6,column=4)

BG_calibrate = tk.Button(root, text="Cal", font=fontStyle,
                          command = lambda:calibrate(BG_text, 0x14, 0xc0, 0x00, 0xcf, 0xff, BG))
BG_calibrate.grid(row=6, column=5)
    
# INIT PD
PD = PowerSupply(3.3, False,0,0)
PD_text = "PD"
button_PD = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_PD, PD_text, PD, 0x40, 0x00))
button_PD.grid(row=7, column=3)
    
PD_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
PD_voltage_entry.grid(row=7, column=1)
    
PD_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(PD, PD_voltage_entry, PD_text))
PD_submit.grid(row=7,column=4)

PD_calibrate = tk.Button(root, text="Cal", font=fontStyle,
                          command = lambda:calibrate(PD_text, 0x15, 0xd0, 0x00, 0xdf, 0xff, PD))
PD_calibrate.grid(row=7, column=5)

# INIT 2.5V
V2_5 = PowerSupply(3.3, False,0,0)
V2_5_text = "2.5V"
button_V2_5 = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_V2_5, V2_5_text, V2_5, 0x80, 0x00))
button_V2_5.grid(row=8, column=3)
    
V2_5_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
V2_5_voltage_entry.grid(row=8, column=1)
    
V2_5_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(V2_5, V2_5_voltage_entry, V2_5_text))
V2_5_submit.grid(row=8,column=4)

V2_5_calibrate = tk.Button(root, text="Cal", font=fontStyle,
                          command = lambda:calibrate(V2_5_text, 0x16, 0xe0, 0x00, 0xef, 0xff, V2_5))
V2_5_calibrate.grid(row=8, column=5)

# INIT 1.8V
V1_8 = PowerSupply(1.8, False,0,0)
V1_8_text = "1.8V"
button_V1_8 = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_V1_8, V1_8_text, V1_8, 0x1D, 0x1C))
button_V1_8.grid(row=9, column=3)
    
V1_8_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
V1_8_voltage_entry.grid(row=9, column=1)
    
V1_8_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(V1_8, V1_8_voltage_entry, V1_8_text))
V1_8_submit.grid(row=9,column=4)

V1_8_calibrate = tk.Button(root, text="Cal", font=fontStyle,
                          command = lambda:calibrate(V1_8_text, 0x17, 0xf0, 0x00, 0xff, 0xff, V1_8))
V1_8_calibrate.grid(row=9, column=5)
    
# INIT 1.2V
V1_2 = PowerSupply(1.0, False,0,0)
V1_2_text = "1.2V"
button_V1_2 = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_V1_2, V1_2_text, V1_2))
button_V1_2.grid(row=10, column=3)
    
V1_2_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
V1_2_voltage_entry.grid(row=10, column=1)
    
V1_2_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(V1_2, V1_2_voltage_entry, 0x00, 0x00, V1_2_text))
V1_2_submit.grid(row=10,column=4)

# main
init()
init_labels()
root.mainloop()
