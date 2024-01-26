#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#cardreader
from tests.cardReaderTest import CardReader
import time
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#oledDisplay
from machine import Pin, I2C
from source.sh1106 import SH1106_I2C
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#jason datei
import json


class App():
    def __init__(self):
        
        self.CardId  = None
        self.Balance = None
        
    def run():
        
        while True:
            pass
            #Lesen der Karte
            # Wenn gefunden in self.Car.. self.Bal
            
            #Wenn neueCard = self.Car timeout auf 5 sec
            #Wenn neueCard andere dann self.Car = neueCard und timeout auf 5
            #oneshotimer auf 5 sec -> resetCard
            uid = cardReader.readfromcard()
      
            uid = uid.get("cardId", None)

            if uid is None:
              #print("No Card")          
              utime.sleep_ms(250)
              continue
            else:
              print(uid)
              
            try:
              with open("sd/accounts.json","r") as file:
                accounts = json.load(file)
            
              self.CardId = uid
              
              if uid in accounts.keys():
                self.Bal    = accounts.get(uid, 0.00)
                #hier auf und entladen  
              else:               
                self.Bal    = 0
                self.NewCardFlag = True
              
            except:
              print("No File")
              with open("sd/accounts.json","w") as file:
                  json.dump({}, file)
            
    def resetCard(self):
        self.CardId = None
        self.Balance= None
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#init display
i2c=I2C(0,sda=Pin(16), scl=Pin(17), freq=400000)
devices = i2c.scan()
oled = SH1106_I2C(128, 64, i2c,addr=devices[0])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Globale Variablen

Guthaben = 0
flag = False
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#initialisieren von Buttons
from machine import Timer

aufladen = Pin(22, Pin.IN, Pin.PULL_DOWN)
bezahlen = Pin(21, Pin.IN, Pin.PULL_DOWN)
aufladenzehner = Pin(20, Pin.IN, Pin.PULL_DOWN)
kartehinzufügen = Pin(19, Pin.IN, Pin.PULL_DOWN)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




import utime

cardReader = CardReader()

from source.sdCard import SDCard
import uos

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(9, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(10),
                  mosi=machine.Pin(11),
                  miso=machine.Pin(8))

# Initialize SD card
sd = SDCard(spi, cs)

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

print("Init")


while True:
      
      uid = cardReader.readfromcard()
      
      uid = uid.get("cardId", None)
      
      if uid is None:
          #print("No Card")          
          utime.sleep_ms(250)
          continue
      else:
          print(uid)
          
      print("test")
      
      try:
        with open("sd/accounts.json","r") as file:
          accounts = json.load(file)
      except:
          print("No File")
          accounts = {}
      
      #print(uid)
      
