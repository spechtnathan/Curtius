
import machine
import lib.sdcard as sdcard
import uos
import time

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(17, machine.Pin.OUT)


# Initialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(0,
                baudrate=1000000,
                polarity=0,
                phase=0,
                bits=8,
                firstbit=machine.SPI.MSB,
                sck=machine.Pin(18),
                mosi=machine.Pin(19),
                miso=machine.Pin(16))

# Initialize SD card, I know, I know but it is working only with that
sd = sdcard.SDCard(spi, cs)
# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

# Get list filename
files = uos.listdir("/sd")

print(files)

def save_line(self, msg, bu):
    """Appends a line to the specified file on the SD card."""
    with open(f"/sd/{self.filename}.sav", "a") as file:
        file.write(msg + "\r\n")
    with open(f"/sd/bu_{self.filename}.sav", "a") as file:
        file.write(bu + "\r\n")

def read_lines_bu(self, a, b):
    with open(f"/sd/bu_{self.filename}", 'r') as file: 
        lines = []
        for i, line in enumerate(file): 
            if a <= i <= b:  # Read lines 3 to 5 (0-indexed) 
                lines.append(line.strip())

        return lines
        
def read_lines(self, a, b):
    with open(f"/sd/{self.filename}", 'r') as file: 
        lines = []
        for i, line in enumerate(file): 
            if a <= i <= b:  # Read lines 3 to 5 (0-indexed) 
                lines.append(line.strip())

        return lines