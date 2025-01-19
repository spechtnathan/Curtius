from machine import Pin
import time
p = Pin(15, Pin.OUT)
p.on()
i = 0

while(True):
    p.toggle()
    time.sleep(1 - i * 0.01)
    i += 1