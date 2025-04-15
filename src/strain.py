from machine import ADC, Pin

class STRAIN:
    def __init__(self): # initialize the MPU 9250, accelerometer
        self.pin1 = ADC(Pin(26))
        self.pin2 = ADC(Pin(27))
    
    def get_values(self):
        return(self.pin1.read_u16(), self.pin2.read_u16())