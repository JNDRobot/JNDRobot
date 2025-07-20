from machine import Pin
import neopixel
import time

def demo(np):
    n = np.n    # считаем количество светодиодов
    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

leds = 8	# количество светодиодов
GPIO_WS2812 = 16 # порт к которому подключены светодиоды
pin = Pin(GPIO_WS2812, Pin.OUT)	# информационный вывод(DIN) к которому подключены светодиоды настраиваем на выход
np = neopixel.NeoPixel(pin, leds) #создаем объект neopixel

#brightness :0-255
brightness=5 #яркость

red = [brightness, 0, 0]
green = [0,brightness,0]                   
blue = [0,0,brightness]                    
white = [brightness,brightness,brightness] 
off = [0,0,0]
yellow = [brightness, brightness, 0]

colors = [red, green, blue, white, yellow]

brightness = 5

demo(np)

while True:
    np[0] = blue
    np.write()

red = [brightness, 0, 0]
np.fill(yellow)
np.write()
while(True):
    pass
    
    
