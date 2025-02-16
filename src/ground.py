from machine import SPI, Pin
from lib.rfm69 import RFM69
import time
import args
import struct

class GROUND:
    def __init__(self):
        spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4), baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
        nss = Pin( 5, Pin.OUT, value=True )
        rst = Pin( 3, Pin.OUT, value=False )

        self.rfm = RFM69( spi=spi, nss=nss, reset=rst )
        self.rfm.frequency_mhz = args.FREQ
        self.rfm.encryption_key = ( args.ENCRYPTION_KEY )
        self.rfm.node = args.BASESTATION_ID

        print( 'Freq            :', self.rfm.frequency_mhz )
        print( 'NODE            :', self.rfm.node )

        print("Waiting for packets...")

        self.temperature = 0
        self.pressure = 0
        self.strain1 = 0
        self.strain2 = 0
        self.lat = 0
        self.lon = 0
        self.alt = 0
        self.ax = 0
        self.ay = 0
        self.az = 0
    
    def loop(self):
        packet = self.rfm.receive( timeout=0.5 ) # Without ACK
        if packet is None: # No packet received
            print( "." )
            pass
        else: # Received a packet!
            # And decode from struct packets

            packet_id = packet[0]  # First byte is the packet ID
            
            if packet_id == 1:  # Critical Data (Temp, Humidity, Pressure, Voltage, Altitude)
                id, self.temperature, self.pressure = struct.unpack("Bff", packet)
                #print(f"[Weather] Temp: {temperature}, Pres: {pressure}")
            
            elif packet_id == 2:  # IMU Data (Gyroscope + Acceleration)
                id, self.strain1, self.strain2, self.ax, self.ay, self.az = struct.unpack("Bfffff", packet)
                #print(f"[Strain] 1: {strain1}, 2: {strain2}")
            
            elif packet_id == 3:  # Magnetometer Data
                id, self.lat, self.lon, self.alt = struct.unpack("Bfff", packet)
                #print(f"[Space] Lat: {lat}, Lon: {lon}, Alt: {alt}, Ax: {ax}, Ay: {ay}, Az: {az},")

            elif packet_id == 4:  # No position
                
                print("no position")

            else:
                print(f"Unknown packet ID: {packet_id}")

            rssi = str(self.rfm.last_rssi) # signal strength
            print(f"{rssi}\t{self.temperature}\t{self.pressure}\t{self.strain1}\t{self.strain2}\t{self.lat}\t{self.lon}\t{self.alt}\t{self.ax}\t{self.ay}\t{self.az}") # print message with signal strength


