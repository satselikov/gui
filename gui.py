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


status = False
def isClicked(button, text, var):
    global status
    status = not status
    if status:
        button["text"] = "OFF"
        var.set_status(False)
        print(text + " status is" , var.get_status())
    else:
        button["text"] = "ON"
        var.set_status(True)
        print(text + " status is" , var.get_status())

class PowerSupply:
    def __init__(self, voltage, status):
        self.voltage = voltage
        self.status = status
    def set_voltage(self, voltage):
        self.voltage = voltage
    def get_voltage(self):
        return self.voltage
    def set_status(self, status):
        self.status = status
    def get_status(self):
        #print(self.status)
        return self.status

def submit(component, entry, bitsON, bitsOFF, text):
    if(component.get_status() == True):
        #print("true within submit")
        submit_helper(text, entry)
        bus.write_byte_data(0x74, 0x02, bitsON)
    else:
        #print("false within submit")
        submit_helper(text, entry)
        bus.write_byte_data(0x74, 0x02, bitsOFF)
    
def submit_helper(text, entry):
    if(len(entry.get()) == 0 ):
        print("Entry for", text, " : None")
    else:
        print("Entry for", text, " :",  entry.get())

def init_TIA():
    TIA = PowerSupply(1.8, False)
    button_TIA = tk.Button(root, text="OFF", font=fontStyle,
        command=lambda:isClicked(button_TIA, "button_TIA", TIA))
    button_TIA.grid(row=1, column=3)

    TIA_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
    TIA_voltage_entry.grid(row=1, column=1)

    TIA_submit = tk.Button(root, text="Submit", font=fontStyle, 
        command=lambda:submit(TIA, TIA_voltage_entry, 0x01, 0x00, "TIA"))
    TIA_submit.grid(row=1,column=4)

def init_LED():
    LED = PowerSupply(4.4, False)
    button_LED = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_LED, "button_LED", LED))
    button_LED.grid(row=2, column=3)
    
    LED_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
    LED_voltage_entry.grid(row=2, column=1)
    
    LED_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(LED, LED_voltage_entry, 0x02, 0x00, "LED"))
    LED_submit.grid(row=2,column=4)

def init_DRV():
    DRV = PowerSupply(1.0, False)
    button_DRV = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_DRV, "button_DRV", DRV))
    button_DRV.grid(row=3, column=3)
    
    DRV_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
    DRV_voltage_entry.grid(row=3, column=1)
    
    DRV_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(DRV, DRV_voltage_entry, 0x04, 0x00, "DRV"))
    DRV_submit.grid(row=3,column=4)

def init_LA():
    LA = PowerSupply(1.0, False)
    button_LA = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_LA, "button_LA", LA))
    button_LA.grid(row=4, column=3)
    
    LA_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
    LA_voltage_entry.grid(row=4, column=1)
    
    LA_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(LA, LA_voltage_entry, 0x08, 0x00, "LA"))
    LA_submit.grid(row=4,column=4)

def init_BF():
    BF = PowerSupply(1.0, False)
    button_BF = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_BF, "button_BF", BF))
    button_BF.grid(row=5, column=3)
    
    BF_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
    BF_voltage_entry.grid(row=5, column=1)
    
    BF_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(BF, BF_voltage_entry, 0x10, 0x00, "BF"))
    BF_submit.grid(row=5,column=4)
    
def init_BG():
    BG = PowerSupply(1.8, False)
    button_BG = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_BG, "button_BG", BG))
    button_BG.grid(row=6, column=3)
    
    BG_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
    BG_voltage_entry.grid(row=6, column=1)
    
    BG_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(BG, BG_voltage_entry, 0x20, 0x00, "BG"))
    BG_submit.grid(row=6,column=4)
    
def init_PD():
    PD = PowerSupply(3.3, False)
    button_PD = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_PD, "button_PD", PD))
    button_PD.grid(row=7, column=3)
    
    PD_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
    PD_voltage_entry.grid(row=7, column=1)
    
    PD_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(PD, PD_voltage_entry, 0x40, 0x00, "PD"))
    PD_submit.grid(row=7,column=4)

def init_V2_5():
    V2_5 = PowerSupply(3.3, False)
    button_V2_5 = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_V2_5, "button_V2_5", V2_5))
    button_V2_5.grid(row=8, column=3)
    
    V2_5_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
    V2_5_voltage_entry.grid(row=8, column=1)
    
    V2_5_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(V2_5, V2_5_voltage_entry, 0x80, 0x00, "2.5V"))
    V2_5_submit.grid(row=8,column=4)

def init_V1_8():
    V1_8 = PowerSupply(1.8, False)
    button_V1_8 = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_V1_8, "button_V1_8", V1_8))
    button_V1_8.grid(row=9, column=3)
    
    V1_8_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
    V1_8_voltage_entry.grid(row=9, column=1)
    
    V1_8_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(V1_8, V1_8_voltage_entry, 0x1D, 0x1C, "1.8V"))
    V1_8_submit.grid(row=9,column=4)
    
def init_V1_2():
    V1_2 = PowerSupply(1.0, False)
    button_V1_2 = tk.Button(root, text="OFF", font=fontStyle, 
        command=lambda:isClicked(button_V1_2, "button_V1_2", V1_2))
    button_V1_2.grid(row=10, column=3)
    
    V1_2_voltage_entry = tk.Entry(root, width=5, font=fontStyle)
    V1_2_voltage_entry.grid(row=10, column=1)
    
    V1_2_submit = tk.Button(root, text="Submit", font=fontStyle,
        command=lambda:submit(V1_2, V1_2_voltage_entry))
    V1_2_submit.grid(row=10,column=4)

init()
init_labels()
init_TIA()
init_LED()
init_DRV()
init_LA()
init_BF()
init_BG()
init_PD()
init_V2_5()
init_V1_8()
init_V1_2()
root.mainloop()
