from machine import Pin, ADC
from time import sleep

bat_level = ADC(Pin(26))

while True:
  bat_value = bat_level.read_u16() # read value, 0-65535 across voltage range 0.0v - 3.3v
  print(f'АЦП12345 ADC = {bat_value} BatV = {bat_value * 3.3 / 0xFFFF * 4}')
  
  sleep(1)