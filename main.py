#cardreader
from readtest import ComClass
import time

#oledDisplay
from machine import Pin, I2C
from sh1106 import SH1106_I2C

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#jason datei
import json
with open("accounts.json","r") as file:
    accounts = json.load(file)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#init display
i2c=I2C(0,sda=Pin(16), scl=Pin(17), freq=400000)
devices = i2c.scan()
oled = SH1106_I2C(128, 64, i2c,addr=devices[0])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#jason datei initialisieren





while True:
      
      uid = ComClass.readfromcard(1)
      print(uid)
      
      if str(uid) in accounts:
         #guthaben aus liste laden 
         a=accounts[str(uid)]
         print(a)
         
         #guthabenauf und entladen
         a=a+1
         print(a)
         
         #liste updaten
         accounts.update({str(uid):a})

          
         oled.fill(0)
         oled.text(str(uid), 0, 0)
         oled.text(str(a),0,30)
         oled.show()
         time.sleep(0.5)
#      else:
#          oled.fill(0)
#          oled.text(str("neue Karte!"),0,0)
#          oled.show()
#          #if knopf 4 gedrückt
#          time.sleep(2)
 #         accounts.update({str(uid):a})
 #         oled.fill(0)
 #         oled.text(str(uid),0,0)
 #         oled.show()
 #         time.sleep(2)
          
    
