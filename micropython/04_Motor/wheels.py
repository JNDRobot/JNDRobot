
from machine import Pin
from machine import PWM
import utime

'''
Class to represent our robot car
'''

# [M1_IN1, M1_IN2, M2_IN1, M2_IN2, M3_IN1, M3_IN2, M4_IN1, M4_IN2]

class OrdinaryWheels:
    MAX_DUTY_CYCLE = 0xFFFF
    MIN_DUTY_CYCLE = 0
    def __init__(self, motor_pins, frequency=20000):
        self.lf_pin1 = PWM(Pin(motor_pins[0], mode=Pin.OUT))
        self.lf_pin2 = PWM(Pin(motor_pins[1], mode=Pin.OUT))
        self.lb_pin1 = PWM(Pin(motor_pins[2], mode=Pin.OUT))
        self.lb_pin2 = PWM(Pin(motor_pins[3], mode=Pin.OUT))

        self.rf_pin1 = PWM(Pin(motor_pins[4], mode=Pin.OUT))
        self.rf_pin2 = PWM(Pin(motor_pins[5], mode=Pin.OUT))
        self.rb_pin1 = PWM(Pin(motor_pins[6], mode=Pin.OUT))
        self.rb_pin2 = PWM(Pin(motor_pins[7], mode=Pin.OUT))

        # set PWM frequency
        self.lf_pin1.freq(frequency)
        self.lf_pin2.freq(frequency)
        self.lb_pin1.freq(frequency)
        self.lb_pin2.freq(frequency)

        self.rf_pin1.freq(frequency)
        self.rf_pin2.freq(frequency)
        self.rb_pin1.freq(frequency)
        self.rb_pin2.freq(frequency)
        
        self.current_speed = int(OrdinaryWheels.MAX_DUTY_CYCLE / 5)
    
    #+++++forward+++++
    def lf_forward(self, speed):
        self.lf_pin1.duty_u16(self.current_speed)
        self.lf_pin2.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)

    def rf_forward(self, speed):
        self.rf_pin1.duty_u16(self.current_speed)
        self.rf_pin2.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)

    def lb_forward(self, speed):
        self.lb_pin1.duty_u16(self.current_speed)
        self.lb_pin2.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)

    def rb_forward(self, speed):
        self.rb_pin1.duty_u16(self.current_speed)
        self.rb_pin2.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)
    #-----forward-----

    #+++++backward+++++
    def lf_backward(self, speed):
        self.lf_pin1.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)
        self.lf_pin2.duty_u16(self.current_speed)

    def lb_backward(self, speed):        
        self.lb_pin1.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)
        self.lb_pin2.duty_u16(self.current_speed)
    
    def rf_backward(self, speed):
        self.rf_pin1.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)
        self.rf_pin2.duty_u16(self.current_speed)
    
    def rb_backward(self, speed):
        self.rb_pin1.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)
        self.rb_pin2.duty_u16(self.current_speed)
    #-----backward-----

    #+++++stop+++++
    def lf_stop(self):
        self.lf_pin1.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)
        self.lf_pin2.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)

    def lb_stop(self):
        self.lb_pin1.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)
        self.lb_pin2.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)

    def rf_stop(self):
        self.rf_pin1.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)
        self.rf_pin2.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)

    def rb_stop(self):        
        self.rb_pin1.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)
        self.rb_pin2.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)        
    #-----stop-----

    def move_forward(self):
        self.lf_forward(self.current_speed)
        self.rf_forward(self.current_speed)
        self.lb_forward(self.current_speed)
        self.rb_forward(self.current_speed)

    def move_backward(self):
        self.lf_backward(self.current_speed)
        self.rf_backward(self.current_speed)
        self.lb_backward(self.current_speed)
        self.rb_backward(self.current_speed)

    def move_right(self):
        self.lf_forward(self.current_speed)
        self.rf_backward(self.current_speed)
        self.lb_backward(self.current_speed)
        self.rb_forward(self.current_speed)

    def move_left(self):
        self.lf_backward(self.current_speed)
        self.rf_forward(self.current_speed)
        self.lb_forward(self.current_speed)
        self.rb_backward(self.current_speed)

    def turn_left(self):
        self.lf_pin1.duty_u16(self.current_speed)
        self.lf_pin2.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)
        self.lb_pin1.duty_u16(OrdinaryWheels.MAX_DUTY_CYCLE)
        self.lb_pin2.duty_u16(OrdinaryWheels.MAX_DUTY_CYCLE)
        
    def turn_right(self):
        self.lf_pin1.duty_u16(OrdinaryWheels.MAX_DUTY_CYCLE)
        self.lf_pin2.duty_u16(OrdinaryWheels.MAX_DUTY_CYCLE)
        self.lb_pin1.duty_u16(self.current_speed)
        self.lb_pin2.duty_u16(OrdinaryWheels.MIN_DUTY_CYCLE)
        
    def stop(self):
        self.lf_stop()
        self.lb_stop()
        self.rf_stop()
        self.rb_stop()
        

    ''' Map duty cycle values from 0-100 to duty cycle 40000-65535 '''
    def __map_range(self, x, in_min, in_max, out_min, out_max):
      return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
        
    ''' new_speed is a value from 0% - 100% '''
    def change_speed(self, new_speed):
        new_duty_cycle = self.__map_range(new_speed, 0, 100, 40000, 65535)
        self.current_speed = new_duty_cycle

        
    def deinit(self):
        """deinit PWM Pins"""
        print("Deinitializing PWM Pins")
        self.stop()
        utime.sleep(0.1)
        self.lf_pin1.deinit()
        self.lf_pin2.deinit()
        self.lb_pin1.deinit()
        self.lb_pin2.deinit()
        
