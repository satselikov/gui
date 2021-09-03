import PowerSupply

#testing method used to hard code LED
def LEDfunc():
    print("pressed led")
    bus.write_byte_data(0x74, 0x02, 0x02)
    bus.write_byte_data(0x2f, 0x1c, 0x03) #unlocks the POT
    bus.write_byte_data(0x2f, 0x04, 0x14)
    
def LED_sub(component, entry, text, address, bus):
    """
    special case submit for LED 10 bits altered instead of 16,
    POT activation towards the end as well

    Args:
        component: LED object instance variable from p.PowerSupply class
        entry: voltage entry grabbed from user input
        text: "LED"
        address: 0x2f 
    """
    if(len(entry.get()) == 0 ):
        print("Entry for", text, " : None")
    else:
        component.set_voltage(entry.get())
        print("Entry for", text, " :",  entry.get())
    
    voltage = component.get_voltage()
    slope = component.get_slope()
    offset = component.get_offset()

    DAC = float(voltage) * float(slope) + float(offset) #calc dac
    DAC = int(DAC)
    DAC = hex(DAC)
    data_to_write = 0x0400 | int(DAC, 16)

    data_to_write = hex(data_to_write) #conv to hex after |

    data_to_write = data_to_write[2:] #take off 0x
    data_to_write = "0" + data_to_write #add 0 to the front 
    
    data_to_write_1 = data_to_write[:2] #part 1 
    data_to_write_2 = data_to_write[2:] #part 2

    data_to_write_1 = int(data_to_write_1, 16) #conv back to hex
    data_to_write_2 = int(data_to_write_2, 16) #conv back to hex
    
    bus.write_byte_data(0x2f, 0x1c, 0x03) #unlocks the POT
    bus.write_byte_data(0x2f, data_to_write_1, data_to_write_2) #writes using SMBUS