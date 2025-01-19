from machine import SPI, Pin
from rfm69 import RFM69
import time
import args

spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4), baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )

led = Pin( 25, Pin.OUT )

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = args.FREQ
rfm.encryption_key = ( args.ENCRYPTION_KEY )
rfm.node = args.BASESTATION_ID

print( 'Freq            :', rfm.frequency_mhz )
print( 'NODE            :', rfm.node )

print("Waiting for packets...")
def loop():
    packet = rfm.receive( timeout=0.5 ) # Without ACK
    if packet is None: # No packet received
        print( "." )
        pass
    else: # Received a packet!
        led.on()
        # And decode from ASCII text (to local utf-8)
        message = str(packet, "ascii") # this is our message
        rssi = str(rfm.last_rssi) # signal strength
        print(message + ", " + rssi) # print message with signal strength
        led.off()
