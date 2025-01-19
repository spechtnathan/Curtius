import satellite, ground
from machine import Pin
import time

# Configure pins
led = Pin(25, Pin.OUT) # Onboard LED for clock
identifier_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)  # Using GP0


isSatellite = True
counter = 1
ctime = time.time() # time now

if identifier_pin.value() == 0:
    print("SATELLITE")

else:
    print("GROUND STATION")
    isSatellite = False

while True :
    counter += 1
    led.toggle()
    if(isSatellite) :
        satellite.loop()
    else :
        ground.loop()