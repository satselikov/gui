import extras as extras
        
def submit(component, entry, text, bits, which, bus):
    """
    Submit method - when you click the submit button per component entry
    
    Args:
        component: object instance of the Power Supply class (voltage, status, slope, offset)
        entry: entry value pulled from user input text box
        text: COMPONENT_text EX; "TIA" or "DRV"
        
        Example: 0x11 0x10 0x85 0xca
                bits: 0x10, 2nd group of 8bits to identify component
                      which: 8 to identify component 
    """
    
    extras.print_lines()
    extras.chip_select(0x10, bus)
    
    print("Clicked submit for: ", text)
    
    if(len(entry.get()) == 0 ):
        print("Entry for", text, " : None")
    else:
        component.set_voltage(entry.get())
        print("Entry for", text, " :",  entry.get())
        
#     print("Status: ", component.get_status())
#     print("Slope: ", component.get_slope())
#     print("Offset: ", component.get_offset())
    
    voltage = component.get_voltage()
    slope = component.get_slope()
    offset = component.get_offset()
    
    DAC = float(voltage) * float(slope) + float(offset)
    DAC = int(DAC)
    DAC = hex(DAC) #0x987
    DAC = DAC[2:] #987
    DAC_1 = DAC[:1] #9
    DAC_2 = DAC[1:] #87
    DAC_1 = which + DAC_1 #89
    DAC_1 = "0x" + DAC_1 #convert to hex
    DAC_2 = "0x" + DAC_2
    DAC_1 = int(DAC_1, 16) #convert to int as a hex
    DAC_2 = int(DAC_2, 16)

#     print("Bits(hex): ", hex(bits))
#     print("DAC1: ", bin(DAC_1))
#     print("DAC2: ", bin(DAC_2))
    bus.write_i2c_block_data(0x11, bits, [DAC_1, DAC_2])

def calibrate(component, MIN_DAC, MAX_DAC, min_value, max_value):
    """
    Calibration method called by the cal button
    
    Args:
        Example: TIA_text, 0x10, 0x84, 0xff, 0x8f, 0xff, TIA
        text: COMPONENT_text EX; "TIA" or "DRV"
        MIN_DAC: hex value minimum
        MAX_DAC: hex value maximum
        min_value: float value voltage
        max_value: float value voltage
        component: object instance of the Power Supply class (voltage, status, slope, offset) 
    """
    slope = (MAX_DAC-MIN_DAC)/(max_value - min_value)
    offset = -abs(slope)*min_value+MIN_DAC
    
    component.set_slope(slope)
    component.set_offset(offset)