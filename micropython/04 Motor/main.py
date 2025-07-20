from wheels import OrdinaryWheels
import machine
#import wheels
#from hcsr04 import HCSR04
import utime

# Pico W GPIO Pin
LF_IN1 = 18
LF_IN2 = 19
LB_IN1 = 21
LB_IN2 = 20
RB_IN1 = 7
RB_IN2 = 6
RF_IN1 = 9
RF_IN2 = 8 

motor_pins = [LF_IN1, LF_IN2, LB_IN1, LB_IN2, RF_IN1, RF_IN2, RB_IN1, RB_IN2]

# Create an instance of our robot car
robot_car = OrdinaryWheels(motor_pins, 50)
#robot_car.move_forward()
#robot_car.stop()
print("Start")
if __name__ == '__main__':
     try:
         # Test forward, reverse, stop, turn left and turn right
         print("*********Testing forward, reverse and loop*********")
         for i in range(2):
             print("Moving forward")
             robot_car.move_forward()
             utime.sleep(2)
             print("Moving backward")
             robot_car.move_backward()
             utime.sleep(2)
             print("stop")
             robot_car.stop()
             utime.sleep(2)
             print("turn left")
             robot_car.turn_left()
             utime.sleep(2)
             print("turn right")
             robot_car.turn_right()
             utime.sleep(2)
            
         print("*********Testing speed*********")
         for i in range(2):
             print("Moving at 100% speed")
             robot_car.change_speed(100);
             robot_car.move_forward()
             utime.sleep(2)
           
             print("Moving at 50% speed")
             robot_car.change_speed(50);
             robot_car.move_forward()
             utime.sleep(2)
           
             print("Moving at 20% of speed")
             robot_car.change_speed(20);
             robot_car.move_forward()
             utime.sleep(2)
            
             print("Moving at 0% of speed or the slowest")
             robot_car.change_speed(0);
             robot_car.move_forward()
             utime.sleep(2)
            
         robot_car.deinit()

     except KeyboardInterrupt:
         robot_car.deinit()