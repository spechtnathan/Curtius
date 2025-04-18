import machine
import lib.sdcard as sdcard
import uos
import time

class SAVE:
    def __init__(self):
        # Assign chip select (CS) pin (and start it high)
        self.cs = machine.Pin(13, machine.Pin.OUT)

        self.filename = "0"

        # Initialize SPI peripheral (start with 1 MHz)
        self.spi = machine.SPI(1,
                        baudrate=1000000,
                        polarity=0,
                        phase=0,
                        bits=8,
                        firstbit=machine.SPI.MSB,
                        sck=machine.Pin(10),
                        mosi=machine.Pin(11),
                        miso=machine.Pin(12))

        # Initialize SD card, I know, I know but it is working only with that
        try:
            self.sd = sdcard.SDCard(self.spi, self.cs)
            # Mount filesystem
            self.vfs = uos.VfsFat(self.sd)
            uos.mount(self.vfs, "/sd")
        except Exception as e:
            try:
                time.sleep(1)
                self.sd = sdcard.SDCard(self.spi, self.cs)
                self.vfs = uos.VfsFat(self.sd)
                uos.mount(self.vfs, "/sd")
            except Exception as e:
                try:
                    time.sleep(1)
                    self.sd = sdcard.SDCard(self.spi, self.cs)
                    self.vfs = uos.VfsFat(self.sd)
                    uos.mount(self.vfs, "/sd")
                except Exception as e:
                    pass
        
        # Get list filename
        files = uos.listdir("/sd")
        self.filename = -1

        for file in files:
            if file.endswith(".sav"):
                try:
                    num = int(file[:-4])
                    if num > self.filename:
                        self.filename = num
                except ValueError:
                    pass
        
        self.filename += 1
            

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