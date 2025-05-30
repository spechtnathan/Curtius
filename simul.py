from accelerometer import ACCELEROMETER
from antenne import ANTENNE
from air import AIR
from gps import GPS
from save import SAVE
from strain import STRAIN
import struct
import time
from machine import PWM, Pin

class SATELLITE:

    def __init__(self):
        self.lastPayloadTime = 0

        #PAYLOAD
        self.plCounter = 1
        self.maxStr1, self.maxStr2 = 100, 100
        self.minStr1, self.minStr2 = -100, -100

        self.initError = True
        self.maxAttempt = 3

        self.groundAlt = 0
        self.maxAlt = 0
        self.flightStat = 0
        # 0 = on ground
        # 1 = ascending
        # 2 = descending
        # 3 = retransmetting
        # 4 = landed

        self.startPl = 0
        self.lastPlRetransmitted = 0

        self.working = [False, False, False, False, False, False]
        # [0] = Accelerometer
        # [1] = Air
        # [2] = GPS
        # [3] = RFM69
        # [4] = SD Card
        # [5] = Strain

        #Componants
        while self.initError and self.maxAttempt > 0:
            self.initError = False
            try:
                if not self.working[0]:
                    self.accelerometer = ACCELEROMETER()
                    self.working[0] = True
                    print("[OK] Accelerometer")
            except:
                self.initError = True
                print("No Accelerometer")
            try:
                if not self.working[1]:
                    self.air = AIR()
                    self.working[1] = True
                    print("[OK] BMP280")
            except:
                self.initError = True
                print("No Air Mesure")
            try:
                if not self.working[2]:
                    self.gps = GPS()
                    self.working[2] = True
                    print("[OK] GPS")
            except:
                self.initError = True
                print("No Gps Data")
            try:
                if not self.working[3]:
                    self.antenne = ANTENNE()
                    self.working[3] = True
                    print("[OK] RFM69")
            except:
                self.initError = True
                print("No Transmitter. CRITICAL")
            try:
                if not self.working[4]:
                    self.save = SAVE()
                    self.working[4] = True
                    print("[OK] SD Card")
            except:
                self.initError = True
                print("No Save")
            try:
                if not self.working[5]:
                    self.strain = STRAIN()
                    self.working[5] = True
                    print("[OK] Strain")
            except:
                self.initError = True
                print("No Strain")
            self.maxAttempt -= 1

        self.working[0] = True
        self.working[1] = True
        self.working[2] = True
        self.working[3] = True
        self.working[4] = True
        self.working[5] = True
        

        print("Sending...")

    def getPos(self): # Retreive datas from gps antenna
        global lat, lon, alt
        lat = 50
        lon = 5
        x = time.ticks_ms() / 1000
        alt = -5 / 18 * x * x + 100 / 3 * x

        if(self.maxAlt < alt): # if the altitude is higher than the previous one, we are in flight
            self.maxAlt = alt

        if(self.gps.my_gps.speed[2] < 0.1):
            self.groundAlt = alt
        elif(self.groundAlt + 100 < alt and self.flightStat == 0): # if the altitude is higher than 100m, we are in flight
            self.flightStat = 1
            self.startPl = self.plCounter - 30 # start the payloads
        elif(self.flightStat == 1 and self.maxAlt - 100 > alt):
            self.flightStat = 2
        elif(self.flightStat == 2 and self.groundAlt + 500 > alt):
            self.flightStat = 3
        elif(self.flightStat == 3 and self.gps.my_gps.speed[2] < 0.1):
            self.flightStat = 4
            buzzer = PWM(Pin(0))
            buzzer.freq(4600)
            buzzer.duty_u16(65535)
    
    def getAcc(self): # Retreive datas from the accelerometer
        global ax, ay, az
        try:
            ax, ay, az = self.accelerometer.sensor.acceleration
        except:
            ax, ay, az = 1, 2, 3

    def getStrains(self): # Read values from the analogic pins for the strains
        str1, str2 = tuple(v / 65535.0 * 3.3 for v in self.strain.get_values())
        self.maxStr1 = str1 if str1 > self.maxStr1 else self.maxStr1 # only keep the highest/smallest value between two packets incase of short shocks
        self.minStr1 = str1 if str1 < self.minStr1 else self.minStr1
        self.maxStr2 = str2 if str2 > self.maxStr2 else self.maxStr2
        self.minStr2 = str2 if str2 < self.minStr2 else self.minStr2

    def getBMP280(self): # Read values from the BMP280 for weather conditions
        try:
            global tem, pre
            tem, pre =  self.air.raw_values() # read BMP280: Temp, pressure (hPa), humidity
        except:
            global tem, pre
            tem, pre = 1, 2

    def retransmit(self): # Retransmit the last packet if no data was received
        if self.lastPlRetransmitted == 0:
            self.lastPlRetransmitted = self.startPl
        if self.plCounter - self.lastPlRetransmitted < 30:
            self.lastPlRetransmitted = self.startPl
        if self.working[3] and self.working[4]:
            datas = self.save.read_lines(self.lastPlRetransmitted + 1, self.lastPlRetransmitted + 31)
            for data in datas:
                try:
                    self.antenne.send(data)
                except:
                    print("Error in retransmit")
                    pass
        self.lastPlRetransmitted += 31
    def loop(self): # loop of the satellite
        global tem, pre, lat, lon, alt, ax, ay, az
        if self.working[5]:
            self.getStrains() # get strains often to have the max.min.imum mesurements
        if self.working[2]:
            self.gps.updateLoop() # update of the gps

        ctime = time.ticks_ms() # get the current time since launch

        if(ctime - self.lastPayloadTime > 100):  # Send Payloads with 0.1s interval
            self.lastPayloadTime = ctime

            #Send Mesurement
            if(self.plCounter % 4 == 0 and self.working[1]):  # Primary Mission (Temp, Pressure)
                self.getBMP280()
                msg = struct.pack("Biiff", 1, self.plCounter, ctime, tem, pre)
                bu = f"1;{self.plCounter};{ctime};{tem};{pre};;;;;;;;;;"

            elif(self.plCounter % 4 == 1):  # Structure (Strain Reading + Acceleration)
                ax, ay, az = 0, 0, 0 # if no accelerometer, set to 0
                if self.working[0]:
                    self.getAcc()
                
                msg = struct.pack("Biifffffff", 2, 
                                  self.plCounter,
                                  ctime,
                                  self.maxStr1, 
                                  self.maxStr2, 
                                  self.minStr1, 
                                  self.minStr2, 
                                  ax, ay, az)
                bu = f"2;{self.plCounter};{ctime};;;;;;{self.maxStr1};{self.maxStr2};{self.minStr1};{self.minStr2};{ax};{ay};{az}"
                self.maxStr1, self.maxStr2 = -100, -100 # reset max and min
                self.minStr1, self.minStr2 = 100, 100

            elif(self.plCounter % 4 == 2 and self.working[2]):  # GPS
                if True:
                    self.getPos()
                    msg = struct.pack("Biifff", 3, self.plCounter, ctime, lat, lon, alt)
                    bu = f"3;{self.plCounter};{ctime};;;{lat};{lon};{alt};;;;;;;"

            # self.plCounter % 4 == 3:  reserved for the base station

            if(self.plCounter % 4 != 3):
                # Send Packet
                try:
                    if self.working[3]:
                        self.antenne.send(msg)

                    if self.working[4]:
                        self.save.save_line(msg, bu)

                except NameError: # if no data, send an error packet (just 4), :( hope this doesn't happen
                    try:
                        print(f"No data to send : {self.plCounter % 3}")
                        msg = struct.pack("Bii", 4, self.plCounter, ctime)
                        bu = f"4;{self.plCounter};{ctime};;;;;;;;;;;;"
                        if self.working[3]:
                            self.antenne.send(msg)
                        
                        if self.working[4]:
                            self.save.save_line(msg, bu)
                    except:
                        print("No data to send and no antenne or save")
                        pass

            self.plCounter += 1



# Configure pins
led = Pin(25, Pin.OUT) # Onboard LED for clock
led.toggle()
satellite = SATELLITE()
while True:
    led.toggle() # led indicator that shows activity
    satellite.loop()