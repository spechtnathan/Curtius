from accelerometer import ACCELEROMETER
from antenne import ANTENNE
from air import AIR
from gps import GPS
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

        ctime = time.time()

        if(ctime - self.lastPayloadTime > 0.5):  # Send Payload (with 0.5s intervals)
            # Get Mesurement
            self.getPos()
            self.getBMP280()
            self.getAcc()

            #Send Mesurement
            if(self.plCounter % 3 == 0): self.antenne.send(struct.pack("Bff", 1, tem, pre))
            if(self.plCounter % 3 == 1): self.antenne.send(struct.pack("Bff", 2, self.maxStr1, self.maxStr2))
            if(self.plCounter % 3 == 2): self.antenne.send(struct.pack("Bffffff", 3, lat, lon, alt, ax, ay, az))

            self.lastPayloadTime = ctime
            self.plCounter += 1