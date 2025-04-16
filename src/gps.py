# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-neo-6m-micropython/

from machine import UART, Pin
from lib.micropyGPS import MicropyGPS

class GPS:
    def __init__(self):
        # Instantiate the micropyGPS object
        self.my_gps = MicropyGPS(0, 'dd')

        # Define the UART pins and create a UART object
        self.gps_serial = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

    def updateLoop(self):
        try:
            while self.gps_serial.any():
                data = self.gps_serial.read()
                for byte in data:
                    stat = self.my_gps.update(chr(byte))
                    """
                    if stat is not None:
                        # Print parsed GPS data
                        print('UTC Timestamp:', self.my_gps.timestamp)
                        print('Date:', self.my_gps.date_string('long'))
                        print('Latitude:', self.my_gps.latitude_string())
                        print('Longitude:', self.my_gps.longitude_string())
                        print('Altitude:', self.my_gps.altitude)
                        print('Satellites in use:', self.my_gps.satellites_in_use)
                        print('Horizontal Dilution of Precision:', self.my_gps.hdop)
                        print()
                    """
                
        except Exception as e:
            print(f"An error occurred: {e}")