import machine
import time
import os
import sdcard

# Définition des broches
SCK = machine.Pin(10)
MOSI = machine.Pin(11)
MISO = machine.Pin(12)
CS = machine.Pin(13, machine.Pin.OUT)

def reset_sd():
    CS.value(1)  # Désélectionner
    time.sleep(0.5)
    CS.value(0)  # Sélectionner
    time.sleep(0.5)

# Désactivation temporaire du CS
CS.value(1)  
time.sleep(0.5)  # Petit délai avant l'initialisation

# Initialisation SPI à une fréquence basse
spi = machine.SPI(1, baudrate=100_000, polarity=0, phase=0, sck=SCK, mosi=MOSI, miso=MISO)


reset_sd()

try:
    # Initialisation de la carte SD
    sd = sdcard.SDCard(spi, CS)
    vfs = os.VfsFat(sd)
    os.mount(vfs, "/sd")
    print("Carte SD montée avec succès")

    # Augmentation du baudrate après initialisation
    spi.init(baudrate=2_000_000)
except Exception as e:
    print("Erreur lors du montage de la carte SD :", e)


try:
    print("Test de lecture SD")
    sd = sdcard.SDCard(spi, CS)
    print("Lecture OK")
except Exception as e:
    print("Carte SD ne répond pas :", e)
