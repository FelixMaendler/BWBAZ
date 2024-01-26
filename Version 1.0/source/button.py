import machine
import utime

class ButtonPressed():
    
  def __init__(self, PinAufladen, PinZahlen, PinAufladen10, PinKarteneu, Balance):
      self.PinA   = PinAufladen
      self.PinZ   = PinZahlen
      self.Pin10  = PinAufladen10
      self.Pinneu = PinKarteneu
      self.Bal    = Balance
      
  def AufundEntladen(self):
      
      print(self.Pin, self.Bal)

if __name__ == "__main__":
    
    button_instance = ButtonPressed(9, 10)
    button_instance.AufundEntladen()