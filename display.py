from machine import Pin, I2C
from sh1106 import SH1106_I2C

i2c=I2C(0,sda=Pin(16), scl=Pin(17), freq=400000)

devices = i2c.scan()
try:
    oled = SH1106_I2C(128, 64, i2c,addr=devices[0])
    oled.text("hello world", 0, 0)
    oled.show()
except Exception as err:
    print(f"Unable to initialize oled: {err}")