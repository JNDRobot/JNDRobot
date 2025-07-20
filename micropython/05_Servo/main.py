from machine import Pin, PWM
import time

# Настройка PWM на выбранном пине (например, GPIO15)
servo_pin = PWM(Pin(13, Pin.OUT))

# Частота для сервопривода обычно 50 Гц (период 20 мс)
servo_pin.freq(50)

# Функция для установки угла (0°–180°)
def set_servo_angle(angle): # Преобразуем угол в ширину импульса (0.5–2.5 мс)
    pulse_width = (angle / 180) * 2 + 0.5  # в миллисекундах
    duty = int((pulse_width  / 20) * 65535)  # преобразуем в значение duty cycle (0–65535)
    servo_pin.duty_u16(duty)

# Пример использования
set_servo_angle(90)  # Установить серву в 90°
time.sleep(2)
set_servo_angle(0)   # Повернуть в 0°
time.sleep(1)
set_servo_angle(180) # Повернуть в 180°
time.sleep(1)





servo_pin.deinit()
