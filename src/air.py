from machine import I2C, Pin
from lib.bme280 import BME280, BMP280_I2CADDR


class AIR:
    def __init__(self): # Initialize BMP 280, for the weather conditions
        # Buses & Pins
        self.i2c = I2C(0, scl=Pin(9), sda=Pin(8)) # initialize the i2c bus on GP9 and GP8

        # BMP280 Module
        self.bmp = BME280(i2c=self.i2c, address=BMP280_I2CADDR) # create a bmp object

    def raw_values(self): # To get temp and humidity
        temp, pressure, humidity =  self.bmp.raw_values # read BMP280: Temp, pressure (hPa), humidity
        return (temp, pressure) #humidity is not mesured by the BMP280