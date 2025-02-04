from lib.rfm69 import RFM69
import args
from machine import SPI, Pin

class ANTENNE:
    def __init__(self):
        # Buses & Pins
        spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4), baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
        nss = Pin(5, Pin.OUT, value=True)
        rst = Pin(3, Pin.OUT, value=False)

        # RFM Module
        self.rfm = RFM69(spi=spi, nss=nss, reset=rst)
        self.rfm.frequency_mhz  = args.FREQ
        self.rfm.encryption_key = (args.ENCRYPTION_KEY)
        self.rfm.node           = args.NODE_ID # This instance is the node 120
        self.rfm.destination    = args.BASESTATION_ID # Send to specific node 100

        # Informations 
        print( 'Frequency     :', self.rfm.frequency_mhz )
        print( 'encryption    :', self.rfm.encryption_key )
        print( 'NODE_ID       :', args.NODE_ID )
        print( 'BASESTATION_ID:', args.BASESTATION_ID )

    def send(self, message):
        self.rfm.send(message)