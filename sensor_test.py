from stepper_class import step_motor
from machine import ADC, Pin
from math import pi
import time

# Open file to log sensor readings
file = open("sensor_test_output.csv", "w")



# Initialize motor (pins are examples)
motor1 = step_motor(0, 1, 2, 3)
motor2 = step_motor(4, 5, 6, 7)

# Set microsteps and PWM for motors
motor1.set_microsteps(8, 30)
motor2.set_microsteps(8, 30)

# Initialize sensor (pins are examples)
s1 = Pin(13, Pin.OUT)
s1.value(1)  # setting the pin to high so we read from a sensor in the middle
sensor = ADC(26)  # Assuming a single analog sensor for simplicity

# Define parameters
circumference = int(140*pi)
wheelbase = int(210*pi)
angle = 180
microsteps = 8


time.sleep(5)


# Calculate steps needed for the desired rotation
steps = int((wheelbase/circumference)*microsteps * 200 * (angle/360))

motor1.set_direction(-1)
motor2.set_direction(1)
for _ in range(steps):
    # Perform steps in forward direction
    motor1.step()
    motor2.step()

    # Log sensor readings
    file.write(str(sensor.read_u16()))
    file.write("\n") 

    time.sleep(0.002)

# Release motors after operation
motor1.release()
motor2.release()

for _ in range(1000):
    file.write(str(sensor.read_u16()))
    file.write("\n") 

    time.sleep(0.002)

# Change direction for reverse rotation
motor1.set_direction(1)
motor2.set_direction(-1)


for _ in range(steps):
    # Perform steps in reverse direction
    motor1.step()
    motor2.step()
    
    # Log sensor readings
    file.write(str(sensor.read_u16()))
    file.write("\n") 

    time.sleep(0.002)

# Release motors after operation
motor1.release()
motor2.release()

# Close the log file
file.close()