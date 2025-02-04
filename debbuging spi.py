import busio
import board
import digitalio

spi = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = digitalio.DigitalInOut(board.GP5)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True  # Ensure CS is high before scanning

if not spi.try_lock():
    print("SPI bus is busy!")
else:
    print("SPI bus ready")
    spi.unlock()
