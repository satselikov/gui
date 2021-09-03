import extras

def adc_voltage_init(channel, entry, text, change, bus):
    """
    ADC voltage init method
    
    Args:
        -channel: select channel for conversion
        -entry: GUI entry to output text
        -text: attach name of component for debugging purposes
    """
    
    if(text.__eq__("LED")):
        extras.chip_select(0x80, bus)
    else:
        extras.chip_select(0x20,bus)                      # Set address A0_AN1 to talk to U25
    bus.write_i2c_block_data(0x11, 0x0b, [0x02, 0x00])    # Enable reference
    bus.write_i2c_block_data(0x11, 0x04, [0x00, change])  # Set all pins as ADC
    bus.write_i2c_block_data(0x11, 0x02, [0x00, channel]) # X channel for conversion
    
    val = bus.read_word_data(0x11, 0x40)                  # Read single channel and convert to voltage

#     print("hex: ", hex(val))

    #parsing
    val = str(hex(val))
    val = val[2:]
    val = missing_zeros(val)
    val = endian_switch(val)
    val = convert_voltage(val)
    val = round(val,3)
    if(text.__eq__("PD") or text.__eq__("2_5") or text.__eq__("LED")): 
        val = val*2
    entry.delete(0, 'end')
    entry.insert(0,val)


def endian_switch(val):
    """
    Helper method for ADC to convert 16 bit hex digit from little endian to big endian
    
    Args:
        -val: hex val to be converted
    """
    val1 = val[:2]
    val2 = val[2:]
    val = val2 + val1
    return val

def convert_voltage(val):
    """
    Helper Method for ADC
    
    Args:
        -val: voltage value to be converted
    """
    val = val[1:]
    return (int(val, 16)*2.5)/0xfff

def missing_zeros(val):
    """
    Adds the leading zeros if the value is only 3,2,1, or 0. Hex must be 4 digits
    
    Example: 0x212 changed to 0x0212
             0x11 changed to 0x0011
             0x4 changed to 0x0004
    
    Args:
        -val: hex val to be converted
    """
    if(len(val) == 3):
        val = '0' + val
    if(len(val) == 2):
        val = '00' + val
    if(len(val) == 1):
        val = '000' + val
    if(len(val) == 0):
        val = '0000' + val
    return val

def adc_current_init(channel, entry, text, change, bus):
    """
    ADC current init method
    
    Args:
        -channel: select channel for conversion
        -entry: GUI entry to output text
        -text: attach name of component for debugging purposes
        -change: change bit when setting pins to ADC
    """
    print("current init test")
    extras.chip_select(0x40, bus)
    bus.write_i2c_block_data(0x11, 0x0b, [0x02, 0x00])      # Enable reference
    bus.write_i2c_block_data(0x11, 0x04, [0x00, change])    # Set all pins as ADC
    bus.write_i2c_block_data(0x11, 0x02, [0x00, channel])   # X channel for conversion
    
    val = bus.read_word_data(0x11, 0x40)                    # Read single channel and convert to voltage
    
    val = str(hex(val))
    val = val[2:]
    val = missing_zeros(val)
    val = endian_switch(val)
    val = convert_voltage(val)
    val = round(val,6)
    #add offset
    if(text.__eq__("TIA") or text.__eq__("DRV") or text.__eq__("LA") or text.__eq__("BF") or text.__eq__("LED")): 
        val = val/50
    if(text.__eq__("BG") or text.__eq__("PD") or text.__eq__("2.5V") or text.__eq__("1.8V")): 
        val = val/250
    val=val*1000
    entry.delete(0, 'end')
    entry.insert(0,val)