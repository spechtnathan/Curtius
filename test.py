from accelerometer import ACCELEROMETER
from antenne import ANTENNE
from air import AIR
from gps import GPS
from save import SAVE
from strain import STRAIN
import struct
import time
from machine import PWM, Pin

lastPayloadTime = 0

#PAYLOAD
plCounter = 1
maxStr1, maxStr2 = 100, 100
minStr1, minStr2 = -100, -100

initError = True
maxAttempt = 3

groundAlt = 0
maxAlt = 0
flightStat = 0
# 0 = on ground
# 1 = ascending
# 2 = descending
# 3 = retransmetting
# 4 = landed

startPl = 0
lastPlRetransmitted = 0

working = [False, False, False, False, False, False]
# [0] = Accelerometer
# [1] = Air
# [2] = GPS
# [3] = RFM69
# [4] = SD Card
# [5] = Strain

print("\n\n\n")
print("Starting TEST Satellite...\n")
print("Initializing components...\n")
print("\n")


#Componants
while initError and maxAttempt > 0:
    initError = False
    try:
        if not working[0]:
            accelerometer = ACCELEROMETER()
            working[0] = True
            print("[OK] Accelerometer")
    except:
        initError = True
        print("No Accelerometer")
    try:
        if not working[1]:
            air = AIR()
            working[1] = True
            print("[OK] BMP280")
    except:
        initError = True
        print("No Air Mesure")
    try:
        if not working[2]:
            gps = GPS()
            working[2] = True
            print("[OK] GPS")
    except:
        initError = True
        print("No Gps Data")
    try:
        if not working[3]:
            antenne = ANTENNE()
            working[3] = True
            print("[OK] RFM69")
    except:
        initError = True
        print("No Transmitter. CRITICAL")
    try:
        if not working[4]:
            save = SAVE()
            working[4] = True
            print("[OK] SD Card")
    except:
        initError = True
        print("No Save")
    try:
        if not working[5]:
            strain = STRAIN()
            working[5] = True
            print("[OK] Strain")
    except:
        initError = True
        print("No Strain")
    maxAttempt -= 1


print("\n\n\n")
print("All components initialized.\n")
print("\n")
print("Test Strains...\n")
print(tuple(v / 65535.0 * 3.3 for v in strain.get_values()))
print("\n")
print("Test Accelerometer...\n")
print(accelerometer.sensor.acceleration)
print("\n")
print("Test BMP280...\n")
print(air.raw_values())
print("\n")
print("Test Save System...\n")
print("Saving a test lines...\n")
msg = struct.pack("Bii", 4, 0, 1234)
print(msg)
bu = f"0;{0};{1234};;;;;;;;;;;;"
print(bu)
save.save_line(msg, bu)

msg = struct.pack("Bii", 4, 1, 1235)
print(msg)
bu = f"0;{1};{1235};;;;;;;;;;;;"
print(bu)
save.save_line(msg, bu)
print("\n")
print("Reading the test lines...\n")
print(save.read_lines(0, 1))
print(save.read_lines_bu(0, 1))
print("\n")
print("Test Sending Data...\n")
antenne.send(msg)
print("\n")
print("Test Sending Data From File...\n")
antenne.send(save.read_lines(0, 0)[0])
print("\n")
print("Test Buzzer...\n")
buzzer = PWM(Pin(0))
buzzer.freq(4600)
buzzer.duty_u16(65535)
time.sleep(5)
buzzer.duty_u16(0)
print("\n")
print("Tests Finished...\n")