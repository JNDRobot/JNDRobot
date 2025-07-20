from machine import Pin
import utime
led = Pin("LED", Pin.OUT)
i = 0
while True:
    led.toggle()
    utime.sleep(1)
    print(i)
    i += 22222
