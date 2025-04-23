
from machine import PWM, Pin
import time

print("Test Buzzer...\n")

buzzer = PWM(Pin(0))
buzzer.freq(4700)
buzzer.duty_u16(30000)
