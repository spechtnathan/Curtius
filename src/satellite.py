from accelerometer import ACCELEROMETER
from antenne import ANTENNE
from air import AIR
from gps import GPS
from save import SAVE
import struct
import time

class SATELLITE:

    def __init__(self):
        self.lastPayloadTime = 0

        #PAYLOAD
        self.plCounter = 1
        self.maxStr1, self.maxStr2 = 0, 0

        #Componants
        self.accelerometer = ACCELEROMETER()
        self.air = AIR()
        self.gps = GPS()
        self.antenne = ANTENNE()
        self.save = SAVE()

        print("Sending...")

    def getPos(self):
        global lat, lon, alt

        lat = self.gps.my_gps.latitude[0]
        lon = self.gps.my_gps.longitude[0]
        alt = self.gps.my_gps.altitude
    
    def getAcc(self):
        global ax, ay, az
        ax, ay, az = self.accelerometer.sensor.acceleration

    def getStrains(self):
        str1 = 0 # INCOMPLETE
        str2 = 0 # INCOMPLETE
        self.maxStr1 = str1 if str1 > self.maxStr1 else self.maxStr1
        self.maxStr1 = str2 if str2 > self.maxStr2 else self.maxStr2

    def getBMP280(self):
        global tem, pre
        tem, pre =  self.air.raw_values() # read BMP280: Temp, pressure (hPa), humidity

    def loop(self):

        self.getStrains() # get strains often to have the maximum mesurement
        self.gps.updateLoop()

        ctime = time.ticks_ms()

        if(ctime - self.lastPayloadTime > 100):  # Send Payload (with 0.5s intervals)
            self.lastPayloadTime = ctime
            # Get Mesurement

            #Send Mesurement
            if(self.plCounter % 3 == 0):
                self.getBMP280()
                msg = struct.pack("Bff", 1, tem, pre)
            elif(self.plCounter % 3 == 1):
                self.getAcc()
                msg = struct.pack("Bfffff", 2, self.maxStr1, self.maxStr2, ax, ay, az)
            elif(self.plCounter % 3 == 2):
                self.getPos()
                msg = struct.pack("Bfff", 3, lat, lon, alt) if alt != 0 else struct.pack("B", 4)

            self.antenne.send(msg)
            self.save.save_line("last test.txt", msg)

            self.plCounter += 1