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
            print("Successfully mounted the sd card first try")
        except Exception as e:
            try:
                time.sleep(1)
                self.sd = sdcard.SDCard(self.spi, self.cs)
                self.vfs = uos.VfsFat(self.sd)
                uos.mount(self.vfs, "/sd")
                print("Successfully mounted the sd card second try")
            except Exception as e:
                try:
                    time.sleep(1)
                    self.sd = sdcard.SDCard(self.spi, self.cs)
                    self.vfs = uos.VfsFat(self.sd)
                    uos.mount(self.vfs, "/sd")
                    print("Successfully mounted the sd card third try")
                except Exception as e:
                    print("Error while mounting the sd card (but it is likely ok idk why) :", e)
        
        # Get list filename
        files = uos.listdir("/sd")
        self.filename = -1

        for file in files:
            if file.endswith(".csv"):
                try:
                    num = int(file[:-4])
                    if num > self.filename:
                        self.filename = num
                except ValueError:
                    pass
        
        self.filename += 1
            

    def save_file(self, text):
        with open(f"/sd/{self.filename}", "w") as file:
            file.write(text)

    def save_line(self, line):
        """Appends a line to the specified file on the SD card."""
        with open(f"/sd/{self.filename}", "a") as file:
            file.write(line + "\r\n")
    
    def read_save(self):
        with open(f"/sd/{self.filename}", "r") as file:
            print(file.read())