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
    
    def loop(self):
        packet = self.rfm.receive( timeout=0.5 ) # Without ACK
        if packet is None: # No packet received
            print( "." )
            pass
        else: # Received a packet!
            # And decode from struct packets

            packet_id = packet[0]  # First byte is the packet ID
            
            if packet_id == 1:  # Critical Data (Temp, Humidity, Pressure, Voltage, Altitude)
                id, temperature, pressure = struct.unpack("Bff", packet)
                print(f"[Weather] Temp: {temperature}, Pres: {pressure}")
            
            elif packet_id == 2:  # IMU Data (Gyroscope + Acceleration)
                id, strain1, strain2 = struct.unpack("Bff", packet)
                print(f"[Strain] 1: {strain1}, 2: {strain2}")
            
            elif packet_id == 3:  # Magnetometer Data
                id, lat, lon, alt, ax, ay, az = struct.unpack("Bffffff", packet)
                print(f"[Space] Lat: {lat}, Lon: {lon}, Alt: {alt}, Ax: {ax}, Ay: {ay}, Az: {az},")
            
            else:
                print(f"Unknown packet ID: {packet_id}")

            rssi = str(self.rfm.last_rssi) # signal strength
            print("[dB] " + rssi) # print message with signal strength
