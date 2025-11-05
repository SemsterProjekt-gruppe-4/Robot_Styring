# Example usage
# - Insert your main loop here, if any, and how you includes your StepperMotor class
from machine import ADC, Timer
from stepper_motor import step_motor
from diff_drive import diffdrive
import time

li = ADC(0)

# fuction to collect data
def save(t):
    with open('log.csv', 'a') as log:
        log.write(str(li.read_u16() * 3.3 /65536)+'\n')


timer = Timer()
timer.init(freq=100, mode=Timer.PERIODIC, callback=save)

# Initialize the stepper motors with their respective GPIO pins
motor1 = step_motor(0,1,2,3)
motor2 = step_motor(4,5,6,7)


# Set PWM duty cycle for both motors
motor1.set_PWM(20)
motor2.set_PWM(20)


# Initialize the differential drive system with the two motors, wheel diameter, and number of microsteps per step
train = diffdrive(motor1, motor2, 267, 20)

time.sleep(2)

# for loop to turn right and left over the black line to
for _ in range(1):
    # Turn right 180 degrees
    train.turn(180,"r")

    # Release motors
    motor1.release()
    motor2.release()
    
    # Turn left 180 degrees
    train.turn(180,"l")
    
    # Release motors    
    motor1.release()
    motor2.release()

# stops the collection of data
timer.deinit()
