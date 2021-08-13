
def chip_select(address):
    master_bits = 0xff
    #master_bits = bus.read_byte_data(0x74, 0x03)
    master_bits = master_bits & address
    print(hex(master_bits))

chip_select(0b0001)
