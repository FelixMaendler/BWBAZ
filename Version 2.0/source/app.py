
import time
import json

import uos

from machine import Timer
from machine import Pin, I2C, SPI

from source.cardReader import CardReader
from source.sh1106     import SH1106_I2C

from source.sdCard     import SDCard






# # Create a file and write something to it
# with open("/sd/test01.txt", "w") as file:
#     file.write("Hello, SD World!\r\n")
#     file.write("This is a test\r\n")
# 
# # Open the file we just created and read from it
# with open("/sd/test01.txt", "r") as file:
#     data = file.read()
#     print(data)


#===============================================================================
#===============================================================================
class App():
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self):
        
        i2c     = I2C(0,sda=Pin(16), scl=Pin(17), freq=400000)        
        devices = i2c.scan()
        
        self.NewCardId     = None
        self.CurrentUser   = ""
        
        self.Display = SH1106_I2C(128, 64, i2c, addr=devices[0])
        
        self.Reader  = CardReader()
        
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
        
        #Buttons zum auf und entladen
        self.ButtonLoadOne = machine.Pin(22, machine.Pin.IN, Pin.PULL_UP)
        self.ButtonLoadOne.irq(trigger = Pin.IRQ_FALLING, handler = self.ButtonLoadOneFunc)
        
        self.ButtonLoadTen = machine.Pin(20, machine.Pin.IN, Pin.PULL_UP)
        self.ButtonLoadTen.irq(trigger = Pin.IRQ_FALLING, handler = self.ButtonLoadTenFunc)
        
        self.ButtonPay	   = machine.Pin(21, machine.Pin.IN, Pin.PULL_UP)
        self.ButtonPay.irq(trigger = Pin.IRQ_FALLING, handler = self.ButtonPayFunc)
        
        self.NewCardGood   = machine.Pin(19, machine.Pin.IN, Pin.PULL_UP)
        #self.NewCardGood.irq(trigger = Pin.IRQ_Falling, handler = self.ButtonNewCardGood)

        # Initialize SD card
        self.SdCard = SDCard(spi, cs)

        # Mount filesystem
        vfs = uos.VfsFat(self.SdCard)
        uos.mount(vfs, "/sd")
        
        self.TimerCard = Timer()
        self.TimerCard.init(period = 100, mode= Timer.PERIODIC, callback = self.checkReader)
        
        
        #
        # Buttons...
    
    # Buchungsbutton
    # ...
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def ButtonLoadOneFunc(self,timer):
        print("Hier")
        TimerLoadOne = Timer()
        TimerLoadOne.init(period = 50, mode = Timer.ONE_SHOT, callback = self.loadBudget, args = (1))
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~      
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def ButtonLoadTenFunc(self,timer):
        TimerLoadTen = Timer()
        TimerLoadTen.init(period = 50, mode = Timer.ONE_SHOT, callback = self.loadBudget, args = (10))
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def ButtonPayFunc(self,timer):
        TimerPay = Timer()
        TimerPay.init(period = 50, mode = Timer.ONE_SHOT, callback = self.loadBudget, args = (-1))
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    def ButtonNewCardGood(self,timer):
#        TimerNewCardGood = Timer()
#        TimerPay.init(period = 50, mode = Timer.ONE_SHOT, callback = self.newCard)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
    def loadBudget(self, budget:int = None):
        #print(budget)

        if self.CurrentUser and budget:
            try:
                with open("/sd/accounts.json", "r") as file:
                    accounts = json.load(file)
                    
                    self.CurrentUser.update({"budget": self.CurrentUser.get("budget") + budget})
                    print("Hier")
                    accounts.update({self.CurrentUser.get("cardId"): self.CurrentUser})
                    
                    with open("/sd/accounts.json", "w") as file:
                       #file.write(json_object)
                        json.dump(accounts, file)
                    
            except Exception as ex:
                 print(ex)
                 print("New Account Error")
                 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def booking(self):
        if self.CurrentUser:
            # Guthaben um 1 verringern in json
            try:
                with open("/sd/accounts.json", "r") as file:
                    accounts = json.load(file)
                    
                    self.CurrentUser.update({"budget": self.CurrentUser.get("budget") - 1})
                    
                    accounts.update({self.CurrentUser.get("cardId"): self.CurrentUser})
                    
                    with open("/sd/accounts.json", "w") as file:
                       #file.write(json_object)
                        json.dump(accounts, file)
                    
            except Exception as ex:
                 print(ex)
                 print("New Account Error")
            
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def newCard(self):
        if self.NewCardId and self.NewCardGood.value():
            pass
            # Karte anlegen
            
            try:
                with open("/sd/accounts.json", "r") as file:
                    accounts = json.load(file)
                    
                    accounts.update({self.NewCardId :
                                     {
                                         "cardId": self.NewCardId,
                                         "budget": 0
                                    }})
                    
                    #json_object = json.dumps(accounts, indent=4)
                    
                    with open("/sd/accounts.json", "w") as file:
                       #file.write(json_object)
                        json.dump(accounts, file)#, ensure_ascii=False, indent=4)
             
            except Exception as ex:
                 print(ex)
                 print("New Account Error")     
   
            self.NewCardId = None
            
            self.Display.fill(0)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def showData(self):
        if self.CurrentUser:
            #print("Hier")
            self.NewCardId = None
            self.Display.fill(0)
            user = self.CurrentUser
            self.Display.text("CardId:   {cardId}".format(**user), 0, 0)                      
            self.Display.text("Guthaben: {budget}".format(**user), 0, 32)
            self.Display.show()
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def run(self):
                
        while True:
            #print(self.ButtonLoadOne.value())
            pass
          #self.checkReader()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def checkReader(self,timer):
          uid = self.Reader.readfromcard()
          
          cardId = uid.get("cardId", None)
          
          # Wenn Karte gefunden
          if cardId:
              
              accounts = {}
              
              try:
                  #self.CurrentCardId
                  with open("/sd/accounts.json", "r") as file:
                      accounts = json.load(file)

              except:
                  print("Read Accounts Error")                  
                
              else:
                  # Karte bekannt
                  if accounts.get(str(cardId), None) is not None:
                      self.CurrentUser = accounts.get(str(cardId), None)
                      print(self.CurrentUser)
                      self.showData()
                      
                      time.sleep(1)
                      #self.loadBudget(10)
                  
                  # Karte unbekannt
                  else:
                      self.NewCardId = cardId
                      
                      self.Display.fill(0)
                      self.Display.text(str("Neue Karte?"), 0, 0)                      
                      self.Display.text(str(cardId), 0, 32)
                      self.Display.show()
                      
                      time.sleep(2)
                      self.newCard()
          
          # Wenn nicht            
          else:
              self.CurrentUser = None
              self.NewCardId   = None
              
              self.Display.fill(0)
              self.Display.show()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
                  
#     file.write("Hello, SD World!\r\n")
#     file.write("This is a test\r\n")
              
              
              # Aus Json Lesen
              
              # Wenn bekannt, dann Auslesen und auf display
              
                  # Wenn guthaben aufladen, aufladne
                  
                  # sonst wenn guthaben entfernen, dann entfernen
              
              # Sonst neue karte?
          
#     #ablauf wenn karte bekannt ist      
#           if str(uid) in accounts and uid:
#               
#              #print("json funkt")
#              Guthaben = accounts[str(uid)]
#              #print(a)
#              #guthabenauf und entladen
#              aufladen.irq(handler=btn_debounce_aufladen, trigger = Pin.IRQ_RISING)
#              bezahlen.irq(handler=btn_debounce_bezahlen, trigger = Pin.IRQ_RISING)
#              aufladenzehner.irq(handler=btn_debounce_aufladenzehner, trigger = Pin.IRQ_RISING)
#              
#              #print(Guthaben)
#              accounts[str(uid)] = Guthaben
#              print(Guthaben)
#              #liste updaten
#              accounts.update({str(uid):Guthaben})
#              
#              with open("accounts.json","w") as file:
#                       json.dump(accounts, file)
# 
#               
#              oled.fill(0)
#              oled.text(str(uid), 0, 0)
#              oled.text(str(Guthaben),0,30)
#              oled.show()
#              time.sleep(0.5)
#              
#     #ablauf wenn Karte nicht bekannt ist         
#           elif uid and not (str(uid) in accounts):
#               if uid:
#                   
#                   oled.fill(0)
#                   oled.text(str("neue Karte!"),0,0)
#                   oled.show()
#                   
#                   on_pressed_kartehinzufugen.irq(handler=btn_debounce_kartehinzufugen, trigger = Pin.IRQ_RISING) 
#                   
#                   if flag:
#                       
#                       accounts.update({str(uid):0})
#                       
#                       time.sleep(0.5)
#                       
#                       with open("accounts.json","w") as file:
#                           json.dump(accounts, file)
#                       
#                       oled.fill(0)
#                       oled.text(str(uid),0,0)
#                       oled.text(str("neue Karte hinzugefügt"),0,10)
#                       oled.show()
#                       
#                       flag = False
#                       
#                       time.sleep(0.5)
# 
#           else:
#               
#               oled.fill(0)
#               oled.text(str("Karte hin halten"),0,0)
#               oled.show()
            
#===============================================================================
#===============================================================================
        
if __name__ == "__main__":
    print("APP-Main")
    
    app = App()
    
    app.run()


# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #cardreader
# from source.cardReader import CardReader
# 
# import time
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #oledDisplay
# from machine import Pin, I2C
# from source.sh1106 import SH1106_I2C
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #jason datei
# import json
# 
# with open("accounts.json","r") as file:
#     accounts = json.load(file)
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# 
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #init display
# i2c=I2C(0,sda=Pin(16), scl=Pin(17), freq=400000)
# devices = i2c.scan()
# oled = SH1106_I2C(128, 64, i2c,addr=devices[0])
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #Globale Variablen
# 
# Guthaben = 0
# flag = False
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #initialisieren von Buttons
# from machine import Timer
# 
# aufladen = Pin(22, Pin.IN, Pin.PULL_DOWN)
# bezahlen = Pin(21, Pin.IN, Pin.PULL_DOWN)
# aufladenzehner = Pin(20, Pin.IN, Pin.PULL_DOWN)
# kartehinzufügen = Pin(19, Pin.IN, Pin.PULL_DOWN)
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# def on_pressed_aufladen(timer):
#     global Guthaben
#     Guthaben = Guthaben + 1;
#     print(Guthaben)
#     print("guthaben aufladen 1")
# 
# def on_pressed_bezahlen(timer):
#     global Guthaben
#     
#     Guthaben = Guthaben - 1;
#     print("guthaben bezahlen 1")
#     
# def on_pressed_aufladenzehner(timer):
#     global Guthaben
#     Guthaben = Guthaben +10;
#     print("guthaben aufladen 10")
#     #return Guthaben
#     
# def on_pressed_kartehinzufugen(timer):
#     global flag
#     flag = True
#     #return flag
# 
# #entprellung
# def btn_debounce_aufladen(pin):
#     #Timer setzen (period in Millisekunden)
#     Timer().init(mode = Timer.ONE_SHOT, period = 550, callback=on_pressed_aufladen args=(10))
# def btn_debounce_bezahlen(pin):
#     Timer().init(mode = Timer.ONE_SHOT, period = 550, callback = on_pressed_bezahlen)
# 
# def btn_debounce_aufladenzehner(pin):
#     Timer().init(mode = Timer.ONE_SHOT, period = 650, callback = on_pressed_aufladenzehner)
# 
# def btn_debounce_kartehinzufugen(pin):
#     Timer().init(mode = Timer.ONE_SHOT, period = 550, callback = on_pressed_kartehinzufugen)
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# 
# while True:
#       

    
