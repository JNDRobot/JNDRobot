from machine import Pin
import utime

#led = Pin("LED", Pin.OUT) # имя "LED" зарезервированно для подключенного светодиода на Pico Pi
led = Pin(0, Pin.OUT)
i = 0
while True:
    led.toggle()    # светодиод меняет свое состояние на противоположное
    # led.value(1)
    # utime.sleep(1)
    # led.value(0)
    utime.sleep(1)
    print(f'The LED is already blinking {i} seconds (Тест)')
    i += 1
