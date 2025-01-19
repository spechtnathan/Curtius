from machine import SPI, I2C, Pin, ADC
from rfm69 import RFM69
from bme280 import BME280, BMP280_I2CADDR
import time
import math
import args
import main

# Buses & Pins
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4), baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
nss = Pin(5, Pin.OUT, value=True)
rst = Pin(3, Pin.OUT, value=False)
i2c = I2C(0, scl=Pin(9), sda=Pin(8)) # initialize the i2c bus on GP9 and GP8

# RFM Module
rfm = RFM69(spi=spi, nss=nss, reset=rst)
rfm.frequency_mhz  = args.FREQ
rfm.encryption_key = (args.ENCRYPTION_KEY)
rfm.node           = args.NODE_ID # This instance is the node 120
rfm.destination    = args.BASESTATION_ID # Send to specific node 100

# BMP280 Module
bmp = BME280(i2c=i2c, address=BMP280_I2CADDR) # create a bmp object

# 


#PAYLOAD
plCounter = 1
lat, lon, alt = 50.464707, 6.188432, 590.0 #values to remove, just for test
tem, pre, hum = 0, 0, 0 #Given by BMP280
maxStr1, maxStr2 = 0, 0 #Strains values

acc = 0.0
Gravity = 9.81
R = 6371000  # Earth radius in meters
vx, vy, vz = 0, 0, 0
x, y = 0, 0

# Informations 
print( 'Frequency     :', rfm.frequency_mhz )
print( 'encryption    :', rfm.encryption_key )
print( 'NODE_ID       :', args.NODE_ID )
print( 'BASESTATION_ID:', args.BASESTATION_ID )
print("iteration_count, time_sec, pressure_hpa, bmp280_temp") # print header

oldtime = main.ctime
lastPayloadTime = 0

def getPos():
    global acc, lat, lon, alt, vz


    # SIMULATE LAUNCH TO REMOVE
    global oldtime
    dt = time.time() - oldtime
    if(time.time()-main.ctime > 10):
        acc = 11.0
    if(alt > 1090):
        acc = -9.81
    
    #vx += ax * dt
    #vy += ay * dt
    vz += acc * dt
    
    #x += vx * dt
    #y += vy * dt
    alt += vz * dt
    
    lat += (y / R) * (180 / math.pi)
    lon += (x / (R * math.cos(math.radians(lat)))) * (180 / math.pi)
    oldtime = time.time()

def getStrains():
    global maxStr1, maxStr2
    str1 = 0 # INCOMPLETE
    str2 = 0 # INCOMPLETE
    maxStr1 = str1 if str1 > maxStr1 else maxStr1
    maxStr1 = str2 if str2 > maxStr2 else maxStr2

def getBMP280():
    temp, pressure, humidity =  bmp.raw_values # read BMP280: Temp, pressure (hPa), humidity

def loop():
    global plCounter
    global lat, lon, alt
    global tem, pre, hum
    global maxStr1, maxStr2

    global lastPayloadTime

    getStrains() # get strains often to have the maximum mesurement 

    if(lastPayloadTime - main.ctime > 0.5):  # Send Payload (with 0.5s intervals)
        # Get Mesurement
        getPos()
        getBMP280()

        #Send Mesurement
        msg = args.PAYLOAD_FORMAT.format(NAME=args.NAME, plCounter=plCounter, lat=lat, lon=lon, alt=alt, tem=tem, pre=pre, hum=hum, maxStr1=maxStr1, maxStr2=maxStr2)

        print(msg) # For testing only to remove

        rfm.send(bytes(msg , "utf-8"))
        lastPayloadTime = main.ctime
        plCounter += 1