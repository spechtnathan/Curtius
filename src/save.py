import machine
import lib.sdcard as sdcard
import uos

class SAVE:
    def __init__(self):
        # Assign chip select (CS) pin (and start it high)
        self.cs = machine.Pin(13, machine.Pin.OUT)

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

        # Initialize SD card
        self.sd = sdcard.SDCard(self.spi, self.cs)

        # Mount filesystem
        self.vfs = uos.VfsFat(self.sd)
        uos.mount(self.vfs, "/sd")

    def save_line(self, filename, line):
        """Appends a line to the specified file on the SD card."""
        with open(f"/sd/{filename}", "a") as file:
            file.write(line + "\r\n")
    
    def read_save(self, filename):
        with open(f"/sd/test", "r") as file:
            print(file.read())