import machine
from save import SAVE
from antenne import ANTENNE
import uos
import time
import struct

save = SAVE()
antenne = ANTENNE()
        
print("Test Save System...\n")

""""
print("Saving a test lines...\n")

for i in range(100):
    msg = struct.pack("Bii", 4, 0, i * 1000)
    bu = f"0;{0};{i * 1000};;;;;;;;;;;;"
    save.save_line(msg, bu)
    print(i)


print("\n")
print("Test Sending Data...\n")
print("\n")
"""
print("Test Sending Data From File...\n")
startPl = 0
lastPlRetransmitted = 0
plCounter = 1000000
for i in range(5):
    if lastPlRetransmitted == 0 or plCounter - lastPlRetransmitted < 30:
        lastPlRetransmitted = startPl
    if True:
        datas = save.read_lines_name(lastPlRetransmitted, lastPlRetransmitted + 30, 4)
        for data in datas:
            try:
                antenne.send(data)
                time.sleep(0.02)  # Adding a small delay to avoid overwhelming the antenna
            except:
                print("Error in retransmit")
                pass
    lastPlRetransmitted += 31
print("\n")