from machine import SPI, Pin
from lib.rfm69 import RFM69
import time
import args
import struct
from gps import GPS

class GROUND:
    def __init__(self): # Initialize ground receiver

        self.lastGPSpostion = 0
        self.lastGPSpostionSatellite = 0
        self.GPSpositionId = 3
        self.lat = 0
        self.lon = 0
        self.alt = 0

        # Pins for the RFM69
        spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4), baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
        nss = Pin( 5, Pin.OUT, value=True )
        rst = Pin( 3, Pin.OUT, value=False )

        # Initialize RFM69
        self.rfm = RFM69( spi=spi, nss=nss, reset=rst )
        self.rfm.frequency_mhz = args.FREQ
        self.rfm.encryption_key = ( args.ENCRYPTION_KEY )
        self.rfm.node = args.BASESTATION_ID

        #Initialize GPS to have the distance to the satellite
        self.gps = GPS()

        print( 'Freq            :', self.rfm.frequency_mhz )
        print( 'NODE            :', self.rfm.node )

        print("Waiting for packets...")
        
    def getPos(self): # Retreive datas from gps antenna
        self.lat = self.gps.my_gps.latitude[0]
        self.lon = self.gps.my_gps.longitude[0]
        self.alt = self.gps.my_gps.altitude
    
    def loop(self):

        self.gps.updateLoop() # update of the gps

        packet = self.rfm.receive( timeout=0.5 ) # Without ACK

        if packet is None: # No packet received
            print( "." )
            pass
        else: # Received a packet!
            # And decode from struct packets

            packet_type = packet[0]  # First byte is the packet Type (Primary Mission / Structure / GPS)
            rssi = str(self.rfm.last_rssi) # signal strength
            
            if packet_type == 1:  # Primary Mission (Temp, Pressure)
                type, id, ctime, temperature, pressure = struct.unpack("Biiff", packet)
                print(f"{type},{id},{ctime/1000},{temperature},{pressure},{rssi}")
            
            elif packet_type == 2:  # Structure (Strain Reading + Acceleration)
                type, id, ctime, maxStr1, maxStr2, minStr1, minStr2, ax, ay, az = struct.unpack("Biifffffff", packet)
                print(f"{type},{id},{ctime/1000},{maxStr1},{maxStr2},{minStr1},{minStr2},{ax},{ay},{az},{rssi}")
            
            elif packet_type == 3:  # GPS
                type, id, ctime, lat, lon, alt = struct.unpack("Biifff", packet)
                self.lastGPSpostionSatellite = ctime
                print(f"{type},{id},{ctime/1000},{lat},{lon},{alt},{rssi}")

            elif packet_type == 4:  # No data (Empty packet)
                type, id, ctime = struct.unpack("Biifff", packet)
                print(f"{type},{id},{ctime/1000},{rssi}")
                pass

            else: # Should not happen
                print(f"Unknown packet ID: {packet_type}")

        ctime = time.ticks_ms() # get the current time since launch

        if(ctime - self.lastGPSpostion > 1000):  # Send GPS Position with 1s interval
            self.lastGPSpostion = ctime

            self.getPos()
            print(f"5,{self.GPSpositionId},{self.lastGPSpostionSatellite/1000},{self.lat},{self.lon},{self.alt}")

            self.GPSpositionId += 4