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
def on_pressed_aufladen(timer):
    global Guthaben
    Guthaben = Guthaben + 1;
    print(Guthaben)
    print("guthaben aufladen 1")

def on_pressed_bezahlen(timer):
    global Guthaben
    
    Guthaben = Guthaben - 1;
    print("guthaben bezahlen 1")
    
def on_pressed_aufladenzehner(timer):
    global Guthaben
    Guthaben = Guthaben +10;
    print("guthaben aufladen 10")
    #return Guthaben
    
def on_pressed_kartehinzufugen(timer):
    global flag
    flag = True
    #return flag

#entprellung
def btn_debounce_aufladen(pin):
    #Timer setzen (period in Millisekunden)
    Timer().init(mode = Timer.ONE_SHOT, period = 550, callback=on_pressed_aufladen)
def btn_debounce_bezahlen(pin):
    Timer().init(mode = Timer.ONE_SHOT, period = 550, callback = on_pressed_bezahlen)

def btn_debounce_aufladenzehner(pin):
    Timer().init(mode = Timer.ONE_SHOT, period = 650, callback = on_pressed_aufladenzehner)

def btn_debounce_kartehinzufugen(pin):
    Timer().init(mode = Timer.ONE_SHOT, period = 550, callback = on_pressed_kartehinzufugen)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import utime

cardReader = CardReader()

import sdcard
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
sd = sdcard.SDCard(spi, cs)

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
      
#ablauf wenn karte bekannt ist      
      if str(uid) in accounts and uid:
          
         #print("json funkt")
         Guthaben = accounts[str(uid)]
         #print(a)
         #guthabenauf und entladen
         aufladen.irq(handler=btn_debounce_aufladen, trigger = Pin.IRQ_RISING)
         bezahlen.irq(handler=btn_debounce_bezahlen, trigger = Pin.IRQ_RISING)
         aufladenzehner.irq(handler=btn_debounce_aufladenzehner, trigger = Pin.IRQ_RISING)
         
         #print(Guthaben)
         accounts[str(uid)] = Guthaben
         print(Guthaben)
         #liste updaten
         accounts.update({str(uid):Guthaben})
         
         print("Write Card")
         with open("sd/accounts.json","w") as file:
                  json.dump(accounts, file)

          
         oled.fill(0)
         oled.text(str(uid), 0, 0)
         oled.text(str(Guthaben),0,30)
         oled.show()
         time.sleep(0.5)
         
#ablauf wenn Karte nicht bekannt ist         
      elif uid and not (str(uid) in accounts):
          if uid:
              
              oled.fill(0)
              oled.text(str("neue Karte!"),0,0)
              oled.show()
              
              #on_pressed_kartehinzufugen.irq(handler=btn_debounce_kartehinzufugen, trigger = Pin.IRQ_RISING) 
              
              if True:
                  
                  accounts.update({str(uid):0})
                  
                  time.sleep(0.5)
                  
                  with open("sd/accounts.json","w") as file:
                      json.dump(accounts, file)
                  
                  oled.fill(0)
                  oled.text(str(uid),0,0)
                  oled.text(str("neue Karte hinzugefügt"),0,10)
                  oled.show()
                  
                  flag = False
                  
                  time.sleep(0.5)

      else:
          
          oled.fill(0)
          oled.text(str("Karte hin halten"),0,0)
          oled.show()
    
