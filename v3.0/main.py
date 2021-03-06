import pigpio
import smbus
from smbus import SMBus
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkFont

import ADC
import clock
import EVB as GUI1
import extras
import LED as l
import PowerSupply as p

# run sudo pigpiod in terminal for clock to work
# works for the hard wired boards ( not the GPIO reset feature)

"""
TODO:
future versions:
    - fix hard coding in the submit + (combine with LED?)
    - update code in cal GUI
    - importing settings from JSON
"""

#define bit masking
TIA_bits = 0x01
LED_bits = 0x02
DRV_bits = 0x04
LA_bits = 0x08
BF_bits = 0x10
BG_bits = 0x20
PD_bits = 0x40
V2_5_bits = 0x80
V1_8_bits = 0x01

#initialize tabs
tab1 = tk.Tk()
tab1.title("Tab Widget")
tabControl = ttk.Notebook(tab1)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text="power")
tabControl.add(tab2, text="i2c")
tabControl.pack(expand=1, fill="both")

fontStyle = tkFont.Font(family="Lucida Grande", size=20)
fontStyle1 = tkFont.Font(family="Lucida Grande", size=9)

#main labels on tab1 Power Supply GUI
ttk.Label(tab1, text="Set V", font=fontStyle).grid(row=0, column=1)
ttk.Label(tab1, text="Status", font=fontStyle).grid(row=0, column=3)

ttk.Label(tab1, text="V", font=fontStyle).grid(row=0, column=6)
ttk.Label(tab1, text="C", font=fontStyle).grid(row=0, column=8)

ttk.Label(tab1, text="TIA", font=fontStyle).grid(row=1, column=0)
ttk.Label(tab1, text="LED", font=fontStyle).grid(row=2, column=0)
ttk.Label(tab1, text="DRV", font=fontStyle).grid(row=3, column=0)
ttk.Label(tab1, text="LA", font=fontStyle).grid(row=4, column=0)
ttk.Label(tab1, text="BF", font=fontStyle).grid(row=5, column=0)
ttk.Label(tab1, text="BG", font=fontStyle).grid(row=6, column=0)
ttk.Label(tab1, text="PD", font=fontStyle).grid(row=7, column=0)
ttk.Label(tab1, text="V2_5", font=fontStyle).grid(row=8, column=0)
ttk.Label(tab1, text="V1_8", font=fontStyle).grid(row=9, column=0)
ttk.Label(tab1, text="Clock", font=fontStyle).grid(row=10, column=0)

#initialize bus
bus = smbus.SMBus(1)
bus2 = smbus.SMBus(4)

status = False
master_bits = 0
def isClicked(button, text, component, bits, mask):
    """
    method used for changing the on/off buttons
    
    Args:
        button: passed as an argument and corresponding button will change to either on or off text
        text: COMPONENT_text EX; "TIA" or "DRV"
        component: object instance of the Power Supply class (voltage, status, slope, offset)
        bits: 0x02 or 0x03 (location)
        mask: set at the top (masks the certain bits)
            TIA_bits = 0x01
            LED_bits = 0x02
            DRV_bits = 0x04
            LA_bits = 0x08
            BF_bits = 0x10
            BG_bits = 0x20
            PD_bits = 0x40
            V2_5_bits = 0x80
            V1_8_bits = 0x01
    """
    global status
    global master_bits 
    status = not status
    
    extras.print_lines()
    extras.chip_select(0x10, bus) #0x10 for DAC
    
    #read off the bits if address is 0x02 or 0x03 to only change bits 
    if bits == 0x03:
        master_bits = bus.read_byte_data(0x74, 0x03)
    if bits == 0x02:
        master_bits = bus.read_byte_data(0x74, 0x02)
        
    if status:
        button["text"] = "OFF"
        component.set_status(False)
        master_bits = master_bits & ~mask
#         print("master_bits: ", master_bits)
#         print("0x03 DAC: ", hex(bus.read_byte_data(0x74, 0x03)))
#         print("0x02 DAC: ", hex(bus.read_byte_data(0x74, 0x02)))
        bus.write_byte_data(0x74, bits, master_bits)
        print(text + " is disabled.")
        print(text + " status is" , component.get_status())
    else:
        button["text"] = "ON"
        component.set_status(True)
        master_bits = master_bits | mask
#         print("master_bits: ", hex(master_bits))
#         print("0x03 DAC: ", hex(bus.read_byte_data(0x74, 0x03)))
#         print("0x02 DAC: ", hex(bus.read_byte_data(0x74, 0x02)))
        bus.write_byte_data(0x74, bits, master_bits)
        print(text + " is enabled.")
        print(text + " status is" , component.get_status())

# INIT TIA
TIA = p.PowerSupply(1.8,False,0,0)
TIA_text = "TIA"
button_TIA = tk.Button(tab1, text="OFF", font=fontStyle,
                       command=lambda:isClicked(button_TIA, TIA_text, TIA, 0x02, TIA_bits))
button_TIA.grid(row=1, column=3) #ON/OFF button, triggers isClicked method

TIA_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
TIA_voltage_entry.grid(row=1, column=1) #user input entry
TIA_voltage_entry.insert(0,1.8)

TIA_submit = tk.Button(tab1, text="Submit", font=fontStyle,
                       command=lambda:GUI1.submit(TIA, TIA_voltage_entry, TIA_text, 0x10, "8", bus))
TIA_submit.grid(row=1,column=4) #submit button used to grab component information 

GUI1.calibrate(TIA, 0x4ff, 0xfff, 1.710, 2.994)

# INIT LED
LED = p.PowerSupply(4.4,False,0,0)
LED_text = "LED"
button_LED = tk.Button(tab1, text="OFF", font=fontStyle,
                       command=lambda:isClicked(button_LED, LED_text, LED, 0x02, LED_bits))
button_LED.grid(row=2, column=3)
    
LED_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
LED_voltage_entry.grid(row=2, column=1)
LED_voltage_entry.insert(0,1.8)
    
LED_submit = tk.Button(tab1, text="Submit", font=fontStyle,
                       command=lambda:l.LED_sub(LED, LED_voltage_entry, LED_text, 0x2f, bus))
LED_submit.grid(row=2,column=4)

GUI1.calibrate(LED, 0x003, 0x014, 0.670, 3.889)

# INIT DRV
DRV = p.PowerSupply(1.0,False,0,0)
DRV_text = "DRV"
button_DRV = tk.Button(tab1, text="OFF", font=fontStyle,
                       command=lambda:isClicked(button_DRV, DRV_text, DRV, 0x02, DRV_bits))
button_DRV.grid(row=3, column=3)
    
DRV_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
DRV_voltage_entry.grid(row=3, column=1)
DRV_voltage_entry.insert(0,1.0)
    
DRV_submit = tk.Button(tab1, text="Submit", font=fontStyle,
                       command=lambda:GUI1.submit(DRV, DRV_voltage_entry, DRV_text, 0x11, "9", bus))
DRV_submit.grid(row=3,column=4)

GUI1.calibrate(DRV, 0x4ff, 0xfff, 1.142, 1.997)

# INIT LA
LA = p.PowerSupply(1.0, False,0,0)
LA_text = "LA"
button_LA = tk.Button(tab1, text="OFF", font=fontStyle,
                      command=lambda:isClicked(button_LA, LA_text, LA, 0x02, LA_bits))
button_LA.grid(row=4, column=3)
    
LA_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
LA_voltage_entry.grid(row=4, column=1)
LA_voltage_entry.insert(0,1.0)
    
LA_submit = tk.Button(tab1, text="Submit", font=fontStyle,
                      command=lambda:GUI1.submit(LA, LA_voltage_entry, LA_text, 0x12, "a", bus))
LA_submit.grid(row=4,column=4)

GUI1.calibrate(LA, 0x4ff, 0xfff, 1.142, 2.001)

# INIT BF
BF = p.PowerSupply(1.0, False,0,0)
BF_text = "BF"
button_BF = tk.Button(tab1, text="OFF", font=fontStyle,
                      command=lambda:isClicked(button_BF, BF_text, BF, 0x02, BF_bits))
button_BF.grid(row=5, column=3)
    
BF_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
BF_voltage_entry.grid(row=5, column=1)
BF_voltage_entry.insert(0,1.0)
    
BF_submit = tk.Button(tab1, text="Submit", font=fontStyle,
                      command=lambda:GUI1.submit(BF, BF_voltage_entry, BF_text, 0x13, "b", bus))
BF_submit.grid(row=5,column=4)

GUI1.calibrate(BF, 0x4ff, 0xfff, 1.143, 2.002)
    
# INIT BG
BG = p.PowerSupply(1.8, False,0,0)
BG_text = "BG"
button_BG = tk.Button(tab1, text="OFF", font=fontStyle,
                      command=lambda:isClicked(button_BG, BG_text, BG, 0x02, BG_bits))
button_BG.grid(row=6, column=3)
    
BG_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
BG_voltage_entry.grid(row=6, column=1)
BG_voltage_entry.insert(0,1.8)
    
BG_submit = tk.Button(tab1, text="Submit", font=fontStyle,
                      command=lambda:GUI1.submit(BG, BG_voltage_entry, BG_text, 0x14, "c", bus))
BG_submit.grid(row=6,column=4)

GUI1.calibrate(BG, 0x4ff, 0xfff,1.711, 2.991)
    
# INIT PD
PD = p.PowerSupply(3.0, False,0,0)
PD_text = "PD"
button_PD = tk.Button(tab1, text="OFF", font=fontStyle,
                      command=lambda:isClicked(button_PD, PD_text, PD, 0x02, PD_bits))
button_PD.grid(row=7, column=3)
    
PD_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
PD_voltage_entry.grid(row=7, column=1)
PD_voltage_entry.insert(0,3.0)
    
PD_submit = tk.Button(tab1, text="Submit", font=fontStyle,
                      command=lambda:GUI1.submit(PD, PD_voltage_entry, PD_text, 0x15,"d", bus))
PD_submit.grid(row=7,column=4)

GUI1.calibrate(PD, 0x9ff, 0xfff,3.057, 3.990)

# INIT 2.5V
V2_5 = p.PowerSupply(3.3, False,0,0)
V2_5_text = "2.5V"
button_V2_5 = tk.Button(tab1, text="OFF", font=fontStyle,
                        command=lambda:isClicked(button_V2_5, V2_5_text, V2_5, 0x02, V2_5_bits))
button_V2_5.grid(row=8, column=3)
    
V2_5_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
V2_5_voltage_entry.grid(row=8, column=1)
V2_5_voltage_entry.insert(0,2.5)
    
V2_5_submit = tk.Button(tab1, text="Submit", font=fontStyle,
                        command=lambda:GUI1.submit(V2_5, V2_5_voltage_entry, V2_5_text, 0x16, "e", bus))
V2_5_submit.grid(row=8,column=4)

GUI1.calibrate(V2_5, 0x9ff, 0xfff,2.776, 3.626)

# INIT 1.8V
V1_8 = p.PowerSupply(1.8, False,0,0)
V1_8_text = "1.8V"
button_V1_8 = tk.Button(tab1, text="OFF", font=fontStyle,
                        command=lambda:isClicked(button_V1_8, V1_8_text, V1_8, 0x03, V1_8_bits))
button_V1_8.grid(row=9, column=3)
    
V1_8_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
V1_8_voltage_entry.grid(row=9, column=1)
V1_8_voltage_entry.insert(0,1.8)
    
V1_8_submit = tk.Button(tab1, text="Submit", font=fontStyle,
                        command=lambda:GUI1.submit(V1_8, V1_8_voltage_entry, V1_8_text, 0x17, "f", bus))
V1_8_submit.grid(row=9,column=4)

GUI1.calibrate(V1_8, 0x4ff, 0xfff,1.708, 2.993)
    
# INIT CLOCK Deafault - 300000
clock_entry = tk.Entry(tab1, width=7, font=fontStyle)
clock_entry.grid(row=10, column=1)

clock_button = tk.Button(tab1, text="OFF", font=fontStyle,
                         command=lambda:clock.click(clock_button))
clock_button.grid(row=10, column=3)

clock_submit = tk.Button(tab1, text="Submit", font=fontStyle,
                        command=lambda:clock.submitclock(clock_entry))
clock_submit.grid(row=10,column=4)


TIA_ADC_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
TIA_ADC_voltage_entry.grid(row=1, column=6)

LED_ADC_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
LED_ADC_voltage_entry.grid(row=2, column=6)

DRV_ADC_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
DRV_ADC_voltage_entry.grid(row=3, column=6)

LA_ADC_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
LA_ADC_voltage_entry.grid(row=4, column=6)

BF_ADC_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
BF_ADC_voltage_entry.grid(row=5, column=6)

BG_ADC_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
BG_ADC_voltage_entry.grid(row=6, column=6)

PD_ADC_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
PD_ADC_voltage_entry.grid(row=7, column=6)

ADC_2_5_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
ADC_2_5_voltage_entry.grid(row=8, column=6)

ADC_1_8_voltage_entry = tk.Entry(tab1, width=5, font=fontStyle)
ADC_1_8_voltage_entry.grid(row=9, column=6)


# INIT read buttons for ADC (can change to one button)
tia_read_voltage_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_voltage_init(0x01, TIA_ADC_voltage_entry, "TIA", 0xff, bus))
tia_read_voltage_button.grid(row=1, column=7)

LED_read_voltage_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_voltage_init(0x08, LED_ADC_voltage_entry, "LED", 0x38, bus))
LED_read_voltage_button.grid(row=2, column=7)

drv_read_voltage_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_voltage_init(0x02, DRV_ADC_voltage_entry, "DRV", 0xff, bus))
drv_read_voltage_button.grid(row=3, column=7)

la_read_voltage_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_voltage_init(0x04, LA_ADC_voltage_entry, "LA", 0xff, bus))
la_read_voltage_button.grid(row=4, column=7)

bf_read_voltage_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_voltage_init(0x08, BF_ADC_voltage_entry, "BF", 0xff, bus))
bf_read_voltage_button.grid(row=5, column=7)

bg_read_voltage_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_voltage_init(0x10, BG_ADC_voltage_entry, "BG", 0xff, bus))
bg_read_voltage_button.grid(row=6, column=7)

pd_read_voltage_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_voltage_init(0x20, PD_ADC_voltage_entry, "PD", 0xff, bus))
pd_read_voltage_button.grid(row=7, column=7)

read25_voltage_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_voltage_init(0x40, ADC_2_5_voltage_entry, "2_5", 0xff, bus))
read25_voltage_button.grid(row=8, column=7)

read18_voltage_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_voltage_init(0x80, ADC_1_8_voltage_entry, "1_8", 0xff, bus))
read18_voltage_button.grid(row=9, column=7)

#single ADC button to call all functions 
# adc_button = tk.Button(tab1, text="Read", font=fontStyle,
#                        command=lambda:[adc_voltage_init(0x01, TIA_ADC_voltage_entry, "TIA"),
#                                        adc_voltage_init(0x02, DRV_ADC_voltage_entry, "DRV"),
#                                        adc_voltage_init(0x04, LA_ADC_voltage_entry, "LA"),
#                                        adc_voltage_init(0x08, BF_ADC_voltage_entry, "BF"),
#                                        adc_voltage_init(0x10, BG_ADC_voltage_entry, "BG"),
#                                        adc_voltage_init(0x20, PD_ADC_voltage_entry, "PD"),
#                                        adc_voltage_init(0x40, ADC_2_5_voltage_entry, "2_5"),
#                                        adc_voltage_init(0x80, ADC_1_8_voltage_entry, "1_8")]
#                        )
# adc_button.grid(row=10, column=6)


TIA_ADC_current_entry = tk.Entry(tab1, width=8, font=fontStyle)
TIA_ADC_current_entry.grid(row=1, column=8)

LED_ADC_current_entry = tk.Entry(tab1, width=8, font=fontStyle)
LED_ADC_current_entry.grid(row=2, column=8)

DRV_ADC_current_entry = tk.Entry(tab1, width=8, font=fontStyle)
DRV_ADC_current_entry.grid(row=3, column=8)

LA_ADC_current_entry = tk.Entry(tab1, width=8, font=fontStyle)
LA_ADC_current_entry.grid(row=4, column=8)

BF_ADC_current_entry = tk.Entry(tab1, width=8, font=fontStyle)
BF_ADC_current_entry.grid(row=5, column=8)

BG_ADC_current_entry = tk.Entry(tab1, width=8, font=fontStyle)
BG_ADC_current_entry.grid(row=6, column=8)

PD_ADC_current_entry = tk.Entry(tab1, width=8, font=fontStyle)
PD_ADC_current_entry.grid(row=7, column=8)

ADC_2_5_current_entry = tk.Entry(tab1, width=8, font=fontStyle)
ADC_2_5_current_entry.grid(row=8, column=8)

ADC_1_8_current_entry = tk.Entry(tab1, width=8, font=fontStyle)
ADC_1_8_current_entry.grid(row=9, column=8)

tia_read_current_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_current_init(0x01, TIA_ADC_current_entry, "TIA", 0xff, bus))
tia_read_current_button.grid(row=1, column=9)

LED_read_current_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_current_init(0x20, LED_ADC_current_entry, "LED", 0x38, bus))
LED_read_current_button.grid(row=2, column=9)

drv_read_current_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_current_init(0x02, DRV_ADC_current_entry, "DRV", 0xff, bus))
drv_read_current_button.grid(row=3, column=9)

la_read_current_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_current_init(0x04, LA_ADC_current_entry, "LA", 0xff, bus))
la_read_current_button.grid(row=4, column=9)

bf_read_current_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_current_init(0x08, BF_ADC_current_entry, "BF", 0xff, bus))
bf_read_current_button.grid(row=5, column=9)

bg_read_current_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_current_init(0x10, BG_ADC_current_entry, "BG", 0xff, bus))
bg_read_current_button.grid(row=6, column=9)

pd_read_current_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_current_init(0x20, PD_ADC_current_entry, "PD", 0xff, bus))
pd_read_current_button.grid(row=7, column=9)

read25_current_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_current_init(0x40, ADC_2_5_current_entry, "2.5V", 0xff, bus))
read25_current_button.grid(row=8, column=9)

read18_current_button = tk.Button(tab1, text="read", font=fontStyle,
                            command=lambda: ADC.adc_current_init(0x80, ADC_1_8_current_entry, "1.8V", 0xff, bus))
read18_current_button.grid(row=9, column=9)

# i2C GUI
def delete0xxx(entry):
    entry.delete(0, 'end')

def read0xxx(channel, entry):
    bits = bus2.read_byte_data(0x55, channel)
    entry.insert(0,bin(bits))

def write0x00():
    bits = bus2.read_byte_data(0x55, 0x00)
    entry_val = entry_0x00.get()
    keep = format(int(bits), "b")
    keep = keep[:3]
    final = str(keep) + str(entry_val)
    print(int(final,2))
    bus2.write_byte_data(0x55, 0x00, int(final,2))

address_0x00 = tk.Label(tab2, text="0x00")
description_0x00 = tk.Label(tab2, text="bandgap",font=fontStyle1)
entry_0x00 = tk.Entry(tab2, width=5)
input_text_0x00 = tk.Label(tab2, text="5-trimming code",font=fontStyle1)
output_text_0x00 = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x00 = tk.Entry(tab2, width=10)
read_0x00_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x00), read0xxx(0x00, output_blank_0x00)])
write_0x00_button = tk.Button(tab2, text='Write', command=write0x00)

address_0x00.grid(row=0, column=0)
description_0x00.grid(row=0, column=1)
entry_0x00.grid(row=0, column=2)
input_text_0x00.grid(row=1, column=2)
output_text_0x00.grid(row=0, column=6)
output_blank_0x00.grid(row=0, column=7)
read_0x00_button.grid(row=0, column=8)
write_0x00_button.grid(row=0, column=9)

def write0x01():
    #read_byte_data
    bits = bus2.read_byte_data(0x55, 0x01)
    entry_val = entry_0x01_47.get()
    entry_val_2 = entry_0x01_02.get()
    keep = format(int(bits), "b")
    keep = keep[4:5]
    final = str(entry_val) + str(keep) + str(entry_val_2)
    bus2.write_byte_data(0x55, 0x01, int(final,2))

address_0x01 = tk.Label(tab2, text="0x01")
description_0x01 = tk.Label(tab2, text="TIA ref and bias current",font=fontStyle1)
entry_0x01_47 = tk.Entry(tab2,width=4)
entry_0x01_02 = tk.Entry(tab2,width=3)
input_text_0x01 = tk.Label(tab2, text="4-bias control",font=fontStyle1)
input_text_0x01_2 = tk.Label(tab2, text="3-TIA voltage",font=fontStyle1)
output_text_0x01 = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x01 = tk.Entry(tab2, width=10)
read_0x01_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x01), read0xxx(0x01, output_blank_0x01)])
write_0x01_button = tk.Button(tab2, text='Write', command=write0x01)

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

def write0x02():
    bits = bus2.read_byte_data(0x55, 0x02)
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
    bus2.write_byte_data(0x55, 0x02, int(final,2))

address_0x02 = tk.Label(tab2, text="0x02")
description_0x02 = tk.Label(tab2, text="VDD12 ref",font=fontStyle1)
entry_0x02_6 = tk.Entry(tab2,width=1)
entry_0x02_5 = tk.Entry(tab2,width=1)
entry_0x02_4 = tk.Entry(tab2,width=1)
entry_0x02_02 = tk.Entry(tab2,width=3)
input_text_0x02 = tk.Label(tab2, text="1-LEDDRV_PD",font=fontStyle1)
input_text_0x02_2 = tk.Label(tab2, text="1-LED PD",font=fontStyle1)
input_text_0x02_3 = tk.Label(tab2, text="1-TIA_PD",font=fontStyle1)
input_text_0x02_4 = tk.Label(tab2, text="3-VDD12 REF",font=fontStyle1)
output_text_0x02 = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x02 = tk.Entry(tab2, width=10)
read_0x02_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x02), read0xxx(0x02, output_blank_0x02)])
write_0x02_button = tk.Button(tab2, text='Write', command=write0x02)

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

def write0x03():
    bits = bus2.read_byte_data(0x55, 0x03)
    entry_val = entry_0x03_57.get()
    entry_val_2 = entry_0x03_04.get()
    final = str(entry_val) + str(entry_val_2)
    bus2.write_byte_data(0x55, 0x03, int(final,2))

address_0x03 = tk.Label(tab2, text="0x03")
description_0x03 = tk.Label(tab2, text="offset cancellation ref",font=fontStyle1)
entry_0x03_57 = tk.Entry(tab2,width=3)
entry_0x03_04 = tk.Entry(tab2,width=5)
input_text_0x03 = tk.Label(tab2, text="3-o.c swing",font=fontStyle1)
input_text_0x03_2 = tk.Label(tab2, text="5-o.c ref ctrl",font=fontStyle1)
output_text_0x03 = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x03 = tk.Entry(tab2, width=10)
read_0x03_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x03), read0xxx(0x03, output_blank_0x03)])
write_0x03_button = tk.Button(tab2, text='Write', command=write0x03)

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

def write0x04():
    bits = bus2.read_byte_data(0x55, 0x04)
    entry_val = entry_0x04_3.get()
    entry_val_2 = entry_0x04_02.get()
    keep = format(int(bits), "b")
    keep = keep[:4]
    final = str(keep) + str(entry_val) + str(entry_val_2)
    bus2.write_byte_data(0x55, 0x04, int(final,2))

address_0x04 = tk.Label(tab2, text="0x04")
description_0x04 = tk.Label(tab2, text="")
entry_0x04_3 = tk.Entry(tab2,width=1)
entry_0x04_02 = tk.Entry(tab2,width=3)
input_text_0x04 = tk.Label(tab2, text="1-freeze",font=fontStyle1)
input_text_0x04_2 = tk.Label(tab2, text="3-o.c gain",font=fontStyle1)
output_text_0x04 = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x04 = tk.Entry(tab2, width=10)
read_0x04_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x04), read0xxx(0x04, output_blank_0x04)])
write_0x04_button = tk.Button(tab2, text='Write', command=write0x04)

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

def write0x05():
    bits = bus2.read_byte_data(0x55, 0x05)
    entry_val = entry_0x05_04.get()
    keep = format(int(bits), "b")
    keep = keep[:3]
    final = str(keep) + str(entry_val)
    bus2.write_byte_data(0x55, 0x05, int(final,2))

address_0x05 = tk.Label(tab2, text="0x05")
description_0x05 = tk.Label(tab2, text="")
entry_0x05_04 = tk.Entry(tab2,width=5)
input_text_0x05 = tk.Label(tab2, text="5-o.c max",font=fontStyle1)
output_text_0x05 = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x05 = tk.Entry(tab2, width=10)
read_0x05_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x05), read0xxx(0x05, output_blank_0x05)])

address_0x05.grid(row=10, column=0)
description_0x05.grid(row=10, column=1)
entry_0x05_04.grid(row=10, column=2)
input_text_0x05.grid(row=11, column=2)
output_text_0x05.grid(row=10, column=6)
output_blank_0x05.grid(row=10, column=7)
read_0x05_button.grid(row=10, column=8)

def write0x06():
    bits = bus2.read_byte_data(0x55, 0x06)
    entry_val = entry_0x06_04.get()
    keep = format(int(bits), "b")
    keep = keep[:3]
    final = str(keep) + str(entry_val)
    bus2.write_byte_data(0x55, 0x06, int(final,2))

address_0x06 = tk.Label(tab2, text="0x06")
description_0x06 = tk.Label(tab2, text="")
entry_0x06_04 = tk.Entry(tab2,width=5)
input_text_0x06 = tk.Label(tab2, text="5-o.c min",font=fontStyle1)
output_text_0x06 = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x06 = tk.Entry(tab2, width=10)
read_0x06_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x06), read0xxx(0x06, output_blank_0x06)])

address_0x06.grid(row=12, column=0)
description_0x06.grid(row=12, column=1)
entry_0x06_04.grid(row=12, column=2)
input_text_0x06.grid(row=13, column=2)
output_text_0x06.grid(row=12, column=6)
output_blank_0x06.grid(row=12, column=7)
read_0x06_button.grid(row=12, column=8)

def write0x07():
    bits = bus2.read_byte_data(0x55, 0x07)
    entry_val = entry_0x07_07.get()
    final = str(entry_val)
    bus2.write_byte_data(0x55, 0x07, int(final,2))

address_0x07 = tk.Label(tab2, text="0x07")
description_0x07 = tk.Label(tab2, text="")
entry_0x07_07 = tk.Entry(tab2,width=8)
input_text_0x07 = tk.Label(tab2, text="8-o.c channel monitored",font=fontStyle1)
output_text_0x07 = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x07 = tk.Entry(tab2, width=10)
read_0x07_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x07), read0xxx(0x07, output_blank_0x07)])
write_0x07_button = tk.Button(tab2, text='Write', command=write0x07)

address_0x07.grid(row=14, column=0)
description_0x07.grid(row=14, column=1)
entry_0x07_07.grid(row=14, column=2)
input_text_0x07.grid(row=15, column=2)
output_text_0x07.grid(row=14, column=6)
output_blank_0x07.grid(row=14, column=7)
read_0x07_button.grid(row=14, column=8)
write_0x07_button.grid(row=14, column=9)

def write0x08():
    bits = bus2.read_byte_data(0x55, 0x08)
    entry_val = entry_0x08_6.get()
    entry_val_2 = entry_0x08_04.get()
    keep = format(int(bits), "b")
    keep = keep[:1]
    keep1 = format(int(bits), "b")
    keep1 = keep1[2:3]
    final = str(keep) + str(entry_val) + str(keep1) + str(entry_val_2)
    bus2.write_byte_data(0x55, 0x08, int(final,2))

address_0x08 = tk.Label(tab2, text="0x08")
description_0x08 = tk.Label(tab2, text="")
entry_0x08_6 = tk.Entry(tab2,width=1)
entry_0x08_04 = tk.Entry(tab2,width=5)
input_text_0x08 = tk.Label(tab2, text="1-global lock",font=fontStyle1)
input_text_0x08_2 = tk.Label(tab2, text="5-o.c DAC level",font=fontStyle1)
output_text_0x08 = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x08 = tk.Entry(tab2, width=10)
read_0x08_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x08), read0xxx(0x08, output_blank_0x08)])

address_0x08.grid(row=16, column=0)
description_0x08.grid(row=16, column=1)
entry_0x08_6.grid(row=16, column=2)
entry_0x08_04.grid(row=16, column=3)
input_text_0x08.grid(row=17, column=2)
input_text_0x08_2.grid(row=17, column=3)
output_text_0x08.grid(row=16, column=6)
output_blank_0x08.grid(row=16, column=7)
read_0x08_button.grid(row=16, column=8)

def write0x09():
    bits = bus2.read_byte_data(0x55, 0x09)
    entry_val = entry_0x09_04.get()
    keep = format(int(bits), "b")
    keep = keep[:3]
    final = str(keep) + str(entry_val)
    bus2.write_byte_data(0x55, 0x09, int(final,2))

address_0x09 = tk.Label(tab2, text="0x09")
description_0x09 = tk.Label(tab2, text="")
entry_0x09_04 = tk.Entry(tab2,width=5)
input_text_0x09 = tk.Label(tab2, text="5-o.c DAC override",font=fontStyle1)
output_text_0x09 = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x09 = tk.Entry(tab2, width=10)
read_0x09_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x09), read0xxx(0x09, output_blank_0x09)])
write_0x09_button = tk.Button(tab2, text='Write', command=write0x09)

address_0x09.grid(row=18, column=0)
description_0x09.grid(row=18, column=1)
entry_0x09_04.grid(row=18, column=2)
input_text_0x09.grid(row=19, column=2)
output_text_0x09.grid(row=18, column=6)
output_blank_0x09.grid(row=18, column=7)
read_0x09_button.grid(row=18, column=8)
write_0x09_button.grid(row=18, column=9)

def write0x0A():
    bits = bus2.read_byte_data(0x55, 0x0A)
    entry_val = entry_0x0A_04.get()
    keep = format(int(bits), "b")
    keep = keep[:3]
    final = str(keep) + str(entry_val)
    bus2.write_byte_data(0x55, 0x0A, int(final,2))

address_0x0A = tk.Label(tab2, text="0x0A")
description_0x0A = tk.Label(tab2, text="LED CONTROL",font=fontStyle1)
entry_0x0A_04 = tk.Entry(tab2,width=5)
input_text_0x0A = tk.Label(tab2, text="5-LED BIAS",font=fontStyle1)
output_text_0x0A = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x0A = tk.Entry(tab2, width=10)
read_0x0A_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x0A), read0xxx(0x0A, output_blank_0x0A)])
write_0x0A_button = tk.Button(tab2, text='Write', command=write0x0A)

address_0x0A.grid(row=20, column=0)
description_0x0A.grid(row=20, column=1)
entry_0x0A_04.grid(row=20, column=2)
input_text_0x0A.grid(row=21, column=2)
output_text_0x0A.grid(row=20, column=6)
output_blank_0x0A.grid(row=20, column=7)
read_0x0A_button.grid(row=20, column=8)
write_0x0A_button.grid(row=20, column=9)

def write0x0B():
    bits = bus2.read_byte_data(0x55, 0x0B)
    entry_val = entry_0x0B_04.get()
    keep = format(int(bits), "b")
    keep = keep[:3]
    final = str(keep) + str(entry_val)
    bus2.write_byte_data(0x55, 0x0B, int(final,2))

address_0x0B = tk.Label(tab2, text="0x0B")
description_0x0B = tk.Label(tab2, text="")
entry_0x0B_04 = tk.Entry(tab2,width=5)
input_text_0x0B = tk.Label(tab2, text="5-LED MOD",font=fontStyle1)
output_text_0x0B = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x0B = tk.Entry(tab2, width=10)
read_0x0B_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x0B), read0xxx(0x0B, output_blank_0x0B)])
write_0x0B_button = tk.Button(tab2, text='Write', command=write0x0B)

address_0x0B.grid(row=22, column=0)
description_0x0B.grid(row=22, column=1)
entry_0x0B_04.grid(row=22, column=2)
input_text_0x0B.grid(row=23, column=2)
output_text_0x0B.grid(row=22, column=6)
output_blank_0x0B.grid(row=22, column=7)
read_0x0B_button.grid(row=22, column=8)
write_0x0B_button.grid(row=22, column=9)

def write0x0C():
    bits = bus2.read_byte_data(0x55, 0x0C)
    entry_val = entry_0x0C_01.get()
    keep = format(int(bits), "b")
    keep = keep[:6]
    final = str(keep) + str(entry_val)
    bus2.write_byte_data(0x55, 0x0C, int(final,2))

address_0x0C = tk.Label(tab2, text="0x0C")
description_0x0C = tk.Label(tab2, text="")
entry_0x0C_01 = tk.Entry(tab2,width=2)
input_text_0x0C = tk.Label(tab2, text="2-LED boost",font=fontStyle1)
output_text_0x0C = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x0C = tk.Entry(tab2, width=10)
read_0x0C_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x0C), read0xxx(0x0C, output_blank_0x0C)])
write_0x0C_button = tk.Button(tab2, text='Write', command=write0x0C)

address_0x0C.grid(row=24, column=0)
description_0x0C.grid(row=24, column=1)
entry_0x0C_01.grid(row=24, column=2)
input_text_0x0C.grid(row=25, column=2)
output_text_0x0C.grid(row=24, column=6)
output_blank_0x0C.grid(row=24, column=7)
read_0x0C_button.grid(row=24, column=8)
write_0x0C_button.grid(row=24, column=9)

def write0x0D():
    bits = bus2.read_byte_data(0x55, 0x0D)
    entry_val = entry_0x0D_04.get()
    keep = format(int(bits), "b")
    keep = keep[:3]
    final = str(keep) + str(entry_val)
    bus2.write_byte_data(0x55, 0x0D, int(final,2))

address_0x0D = tk.Label(tab2, text="0x0D")
description_0x0D = tk.Label(tab2, text="")
entry_0x0D_04 = tk.Entry(tab2,width=5)
input_text_0x0D = tk.Label(tab2, text="5-Input signal reference",font=fontStyle1)
output_text_0x0D = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x0D = tk.Entry(tab2, width=10)
read_0x0D_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x0D), read0xxx(0x0D, output_blank_0x0D)])
write_0x0D_button = tk.Button(tab2, text='Write', command=write0x0D)

address_0x0D.grid(row=26, column=0)
description_0x0D.grid(row=26, column=1)
entry_0x0D_04.grid(row=26, column=2)
input_text_0x0D.grid(row=27, column=2)
output_text_0x0D.grid(row=26, column=6)
output_blank_0x0D.grid(row=26, column=7)
read_0x0D_button.grid(row=26, column=8)
write_0x0D_button.grid(row=26, column=9)

def write0x0E():
    bits = bus2.read_byte_data(0x55, 0x0E)
    entry_val = entry_0x0E_04.get()
    keep = format(int(bits), "b")
    keep = keep[:3]
    final = str(keep) + str(entry_val)
    bus2.write_byte_data(0x55, 0x0E, int(final,2))

address_0x0E = tk.Label(tab2, text="0x0E")
description_0x0E = tk.Label(tab2, text="")
entry_0x0E_04 = tk.Entry(tab2,width=5)
input_text_0x0E = tk.Label(tab2, text="5-Common Mod Ref",font=fontStyle1)
output_text_0x0E = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x0E = tk.Entry(tab2, width=10)
read_0x0E_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x0E), read0xxx(0x0E, output_blank_0x0E)])
write_0x0E_button = tk.Button(tab2, text='Write', command=write0x0E)

address_0x0E.grid(row=28, column=0)
description_0x0E.grid(row=28, column=1)
entry_0x0E_04.grid(row=28, column=2)
input_text_0x0E.grid(row=29, column=2)
output_text_0x0E.grid(row=28, column=6)
output_blank_0x0E.grid(row=28, column=7)
read_0x0E_button.grid(row=28, column=8)
write_0x0E_button.grid(row=28, column=9)

def write0x0F():
    bits = bus2.read_byte_data(0x55, 0x0F)
    entry_val = entry_0x0F_76.get()
    entry_val_2 = entry_0x0F_53.get()
    entry_val_3 = entry_0x0F_21.get()
    entry_val_4 = entry_0x0F_0.get()
    final = str(entry_val) + str(entry_val_2) + str(entry_val_3) + str(entry_val_4)
    bus2.write_byte_data(0x55, 0x0F, int(final,2))

address_0x0F = tk.Label(tab2, text="0x0F")
description_0x0F = tk.Label(tab2, text="")
entry_0x0F_76 = tk.Entry(tab2,width=2)
entry_0x0F_53 = tk.Entry(tab2,width=3)
entry_0x0F_21 = tk.Entry(tab2,width=2)
entry_0x0F_0 = tk.Entry(tab2,width=1)
input_text_0x0F = tk.Label(tab2, text="2-spare bits",font=fontStyle1)
input_text_0x0F_2 = tk.Label(tab2, text="3-test_mux8",font=fontStyle1)
input_text_0x0F_22 = tk.Label(tab2, text="\n0-nothing\n1-REFH\n2-REFL\n3-compref\n4-VDD12ref\n5-DAC1INN\n6-DACINP\n7-VOCMFP",font=fontStyle1)
input_text_0x0F_3 = tk.Label(tab2, text="2-test_mux",font=fontStyle1)
input_text_0x0F_33 = tk.Label(tab2, text="\n0-TIA REF\n1-VBIAS18",font=fontStyle1)
input_text_0x0F_4 = tk.Label(tab2, text="1-Protect LED driver",font=fontStyle1)
output_text_0x0F = tk.Label(tab2, text="output: ",font=fontStyle1)
output_blank_0x0F = tk.Entry(tab2, width=10)
read_0x0F_button = tk.Button(tab2, text='Read', command=lambda:[delete0xxx(output_blank_0x0F), read0xxx(0x0F, output_blank_0x0F)])
write_0x0F_button = tk.Button(tab2, text='Write', command=write0x0F)

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


# main
extras.init(bus)

tab1.mainloop()