class PowerSupply:
    """
    Each component creates an instance of this class.
    Getters and Setters for every variable included.

    Args:
        voltage: from voltage entry box
        status: whether component is on/off
        slope: calculated within calibration and used within submit
        offset: calculated within calibration and used within submit
    """
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