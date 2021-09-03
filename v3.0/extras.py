
def init(bus):
    """
    Initialize the board 
    """
    bus.write_byte_data(0x74, 0x06, 0x00)
    bus.write_byte_data(0x74, 0x07, 0x00)
    bus.write_byte_data(0x74, 0x02, 0x00)
    bus.write_byte_data(0x74, 0x03, 0x0c)
    bus.write_byte_data(0x74, 0x03, 0x1c)
    bus.write_i2c_block_data(0x11, 0x05, [0x00, 0xff])
    bus.write_i2c_block_data(0x11, 0x0b, [0x02, 0x00])
    bus.write_i2c_block_data(0x11, 0x03, [0x00, 0x10])

def print_lines():
    """
    Cleaner method for printing within terminal for serparation purposes
    """
    print("------------------------")

def chip_select(address, bus):
    """
    Method called by DAC + ADC to select chip before any command executed
    """
    master_bits = bus.read_byte_data(0x74, 0x03)
    master_bits = master_bits & 0x0f
    master_bits = master_bits | address
    bus.write_byte_data(0x74, 0x03, master_bits)