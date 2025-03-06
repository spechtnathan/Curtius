from accelerometer import ACCELEROMETER
from antenne import ANTENNE
from air import AIR
from gps import GPS
from save import SAVE
import struct
import time
import random # FOR TESTING

class SATELLITE:

    def __init__(self):
        self.lastPayloadTime = 0

        #PAYLOAD
        self.plCounter = 1
        self.maxStr1, self.maxStr2 = 0, 0
        self.minStr1, self.minStr2 = 0, 0

        #Componants
        self.accelerometer = ACCELEROMETER()
        self.air = AIR()
        self.gps = GPS()
        self.antenne = ANTENNE()
        self.save = SAVE()

        print("Sending...")

    def getPos(self): # Retreive datas from gps antenna
        global lat, lon, alt

        lat = self.gps.my_gps.latitude[0]
        lon = self.gps.my_gps.longitude[0]
        alt = self.gps.my_gps.altitude
    
    def getAcc(self): # Retreive datas from the accelerometer
        global ax, ay, az
        ax, ay, az = self.accelerometer.sensor.acceleration

    def getStrains(self): # Read values from the analogic pins for the strains
        str1 = random.random() * 3.3 # INCOMPLETE (simulated)
        str2 = random.random() * 3.3 # INCOMPLETE
        self.maxStr1 = str1 if str1 > self.maxStr1 else self.maxStr1 # only keep the highest/smallest value between two packets incase of short shocks
        self.minStr1 = str1 if str1 < self.minStr1 else self.minStr1
        self.maxStr2 = str2 if str2 > self.maxStr2 else self.maxStr2
        self.minStr2 = str2 if str2 < self.minStr2 else self.minStr2

    def getBMP280(self): # Read values from the BMP280 for weather conditions
        global tem, pre
        tem, pre =  self.air.raw_values() # read BMP280: Temp, pressure (hPa), humidity

    def loop(self): # loop of the satellite

        self.getStrains() # get strains often to have the max.min.imum mesurements
        self.gps.updateLoop() # update of the gps

        ctime = time.ticks_ms() # get the current time since launch

        if(ctime - self.lastPayloadTime > 100):  # Send Payloads with 0.1s interval
            self.lastPayloadTime = ctime

            #Send Mesurement
            if(self.plCounter % 3 == 0):  # Primary Mission (Temp, Pressure)
                self.getBMP280()
                msg = struct.pack("Biff", 1, self.plCounter, tem, pre)

            elif(self.plCounter % 3 == 1):  # Structure (Strain Reading + Acceleration)
                self.getAcc()
                msg = struct.pack("Bifffffff", 2, self.plCounter, self.maxStr1, self.maxStr2, self.minStr1, self.minStr2, ax, ay, az)
                self.maxStr1, self.maxStr2 = -100, -100 # reset max and min
                self.minStr1, self.minStr2 = 100, 100

            elif(self.plCounter % 3 == 2):  # GPS
                self.getPos()
                msg = struct.pack("Bifff", 3, self.plCounter, lat, lon, alt) if alt != 0 else struct.pack("B", 4)

            # Send Packet
            self.antenne.send(msg)
            # Save system INCOMPLETE (saves a struct and not lines of text)
            self.save.save_line("last test.txt", msg)

            self.plCounter += 1