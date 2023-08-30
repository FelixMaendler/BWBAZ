###########################################################################
# Bauwagenbezahlsystem Version 3.0
#
# Unterprogramm zur Sicherung von Daten
#
#
###########################################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import machine
import sdcard
import uos
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SDData():
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  def __init__(self):
    CS = machine.Pin(9, machine.Pin.OUT)
    spi = machine.SPI(1,baudrate=1000000,
                  polarity=0,phase=0,bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(10),
                  mosi=machine.Pin(11),
                  miso=machine.Pin(8))
    #SD-Karte initialisieren
    sd = sdcard.SDCard(spi,CS) 

    #Filesystem mounten
    vfs = uos.VfsFat(sd)
    uos.mount(vfs, "/sd")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def SDsave(self):
    # Create a file and write something to it
    with open("/sd/hello.txt", "w") as file:
      print("Writing to data.txt...")
      file.write("Welcome to microcontrollerslab!\r\n")
      file.write("This is a test\r\n")

    # Open the file we just created and read from it
    with open("/sd/hello.txt", "r") as file:
      print("Reading data.txt...")
      data = file.read()
      print(data)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SDData.SDsave(1)