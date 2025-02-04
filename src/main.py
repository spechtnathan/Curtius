from machine import Pin
import time
from satellite import SATELLITE
from ground import GROUND

# Configure pins
led = Pin(25, Pin.OUT) # Onboard LED for clock
led.toggle()
identifier_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)  # Using GP0

isSatellite = True
counter = 1


if identifier_pin.value() == 0:
    print("SATELLITE")
    satellite = SATELLITE()

else:
    print("GROUND STATION")
    isSatellite = False
    ground = GROUND()

while True :
    counter += 1
    led.toggle()
    if(isSatellite) :
        satellite.loop()
    else :
        ground.loop()