

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
    
    self.lastCardID = {}
        
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def readfromcard(self):
 
    try:
      state, tag_type = self.reader.request(self.reader.REQIDL)
          
      if state == self.reader.OK:
        
        state, cardUID = self.reader.SelectTagSN()
        
        if state == self.reader.OK:
            
          cardId = int.from_bytes(bytes(cardUID), "little", False)
          
          self.lastCardID = {"cardId": cardId}
          
          return self.lastCardID

      else:
        return {"cardId": self.lastCardID.pop("cardId", None)}

      
    except Exception as ex:
      print(ex)
      return {"error" : "Lese Fehler"}
