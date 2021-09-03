import pigpio
import extras

pi = pigpio.pi() 
status_clock = False
def click(button):
    """
    click method used to activate clock
    
    Args:
        button: clock on/off passed in as a parameter
    """
    global pi
    global status_clock
    status_clock = not status_clock
    extras.print_lines()
    if status_clock:
        button["text"] = "OFF"
        pi.hardware_clock(4, 0)
    else:
        button["text"] = "ON"
        pi.hardware_clock(4, 500000)
        print("Clock is ON")
        print("Default set to 500000")

def submitclock(entry):
    """
    submit helper for clock
    
    Args:
        entry: hz
    """
    global pi
    hz = int(entry.get())
    pi.hardware_clock(4, hz)
    print("clock frequency set to: ", entry.get())