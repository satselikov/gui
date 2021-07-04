import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
#from smbus import SMBus

root = tk.Tk()
#bus = SMBus(1)
fontStyle = tkFont.Font(family="Lucida Grande", size=20)

#main column row labels
voltage_label = tk.Label(root, text="Voltage", font=fontStyle).grid(row = 0, column = 1)
current_label = tk.Label(root, text="Current", font=fontStyle).grid(row = 0, column = 2)
status_label = tk.Label(root, text="Status", font=fontStyle).grid(row = 0, column = 3)


# button_dict = {}
# words = ["TIA", "LED", "DRV", "LA", "BF", "BG", "PD", "2_5V", "1_8V", "1_2V"]

# for index, val in enumerate(words):
# 	button_dict["button_" + val] = tk.Label(root, text="ON", fg = "green", font=fontStyle).grid(row = index+1, column = 4)

# print(button_dict)

status = False
def isClicked(button,text):
    global status
    status = not status

    if status:
        button["text"] = "OFF"
        print(text)
    else:
        button["text"] = "ON"
        print(text)
        
# button_dict = {}
# for index, val in enumerate(words):
# 	print(index, val)
# 	button_dict["button_" + val] = tk.Button(root, text="ON/OFF", font=fontStyle, command=lambda:isClicked(val)).grid(row = index+1, column = 3)

button_TIA = tk.Button(root, text="ON", font=fontStyle, command=lambda:isClicked(button_TIA, "button_tia"))
button_TIA.grid(row=1, column=3)
button_LED = tk.Button(root, text="ON", font=fontStyle, command=lambda:isClicked(button_LED, "button_led"))
button_LED.grid(row=2, column=3)
button_DRV = tk.Button(root, text="ON", font=fontStyle, command=lambda:isClicked(button_DRV, "button_drv"))
button_DRV.grid(row=3, column=3)
button_LA = tk.Button(root, text="ON", font=fontStyle, command=lambda:isClicked(button_LA, "button_la"))
button_LA.grid(row=4, column=3)
button_BF = tk.Button(root, text="ON", font=fontStyle, command=lambda:isClicked(button_BF, "button_bf"))
button_BF.grid(row=5, column=3)
button_BG = tk.Button(root, text="ON", font=fontStyle, command=lambda:isClicked(button_BG, "button_bg"))
button_BG.grid(row=6, column=3)
button_PD = tk.Button(root, text="ON", font=fontStyle, command=lambda:isClicked(button_PD, "button_pd"))
button_PD.grid(row=7, column=3)
button_2_5V = tk.Button(root, text="ON", font=fontStyle, command=lambda:isClicked(button_2_5V, "button_2_5V"))
button_2_5V.grid(row=8, column=3)
button_1_8V = tk.Button(root, text="ON", font=fontStyle, command=lambda:isClicked(button_1_8V, "button_1_8V"))
button_1_8V.grid(row=9, column=3)
button_1_2V = tk.Button(root, text="ON", font=fontStyle, command=lambda:isClicked(button_1_2V, "button_1_2V"))
button_1_2V.grid(row=10, column=3)

label_dict = {}
words = ["TIA", "LED", "DRV", "LA", "BF", "BG", "PD", "2_5V", "1_8V", "1_2V"]
for index, val in enumerate(words):
    label_dict[val] = tk.Label(root, text=val, font=fontStyle).grid(row = index+1, column = 0)


################################################################################
TIA_voltage_entry = tk.Entry(root, width=5, font=fontStyle).grid(row=1, column=1)

LED_voltage_entry = tk.Entry(root, width=5, font=fontStyle).grid(row=2, column=1)

DRV_voltage_entry = tk.Entry(root, width=5, font=fontStyle).grid(row=3, column=1)

LA_voltage_entry = tk.Entry(root, width=5, font=fontStyle).grid(row=4, column=1)

BF_voltage_entry = tk.Entry(root, width=5, font=fontStyle).grid(row=5, column=1)

BG_voltage_entry = tk.Entry(root, width=5, font=fontStyle).grid(row=6, column=1)

PD_voltage_entry = tk.Entry(root, width=5, font=fontStyle).grid(row=7, column=1)

VDD_2_5V_voltage_entry = tk.Entry(root, width=5, font=fontStyle).grid(row=8, column=1)

VDD_1_8V_voltage_entry = tk.Entry(root, width=5, font=fontStyle).grid(row=9, column=1)

VDD_1_2V_voltage_entry = tk.Entry(root, width=5, font=fontStyle).grid(row=10, column=1)

def getfunc():
    butt_list = [button_TIA, button_LED, button_DRV, button_LA, button_BF,button_BG,button_PD,button_2_5V,button_1_8V,button_1_2V]
    entr_list = [TIA_voltage_entry,LED_voltage_entry, DRV_voltage_entry, LA_voltage_entry, BF_voltage_entry, BG_voltage_entry, PD_voltage_entry, VDD_2_5V_voltage_entry, VDD_1_8V_voltage_entry, VDD_1_2V_voltage_entry]
    for index, each in enumerate(butt_list):
        if each["text"] == "ON":
            print(butt_list[index])
            print(entr_list[index])



set_button = tk.Button(root, text="set",font=fontStyle)
set_button.grid(row = 11, column = 3)
get_button = tk.Button(root, text="get",font=fontStyle, command=lambda:getfunc())
get_button.grid(row = 11, column = 4)


root.mainloop()