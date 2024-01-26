
        
from source.cardReader import CardReader

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    
  import utime
  
  cardReader = CardReader()    

  print("Bring TAG closer...")
  print("")

    
  while True:
      
      print(cardReader.readfromcard())
      utime.sleep_ms(100)
      