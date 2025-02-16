from machine import Pin
from satellite import SATELLITE
from ground import GROUND

# Configure pins
led = Pin(25, Pin.OUT) # Onboard LED for clock
led.toggle()
identifier_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)  # Using GP0 to detect if it is the satellite or the ground

isSatellite = True


if identifier_pin.value() == 0: # determine if it is the ground
    print("SATELLITE")
    satellite = SATELLITE()

else:
    print("GROUND STATION")
    isSatellite = False
    ground = GROUND()

while True : # the main loop that goes forever
    led.toggle() # led indicator that shows activity
    if(isSatellite) :
        satellite.loop() # code for the satellite
    else :
        ground.loop() # code for the ground