###########################################################################
# Bauwagenbezahlsystem Version 3.0
#
# Reader
#
#
###########################################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from source.mfrc522 import MFRC522

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CardReader():

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def __init__(self):
    self.reader = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)
    self.reader.init()
        
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def readfromcard(self):
 
    try:
      state, tag_type = self.reader.request(self.reader.REQIDL)
    
      if state == self.reader.OK:
        
        state, cardUID = self.reader.SelectTagSN()
        
        if state == self.reader.OK:
            
          cardId = int.from_bytes(bytes(cardUID), "little", False)
        
          return {"cardId": cardId}
        
    except:
      return {"error" : "Lese Fehler"}

    else:
      return {"error" : "Keine Karte"}
        
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    
  import utime
  
  cardReader = CardReader()    

  print("Bring TAG closer...")
  print("")

    
  while True:
      
      print(cardReader.readfromcard())
      utime.sleep_ms(1000)
      