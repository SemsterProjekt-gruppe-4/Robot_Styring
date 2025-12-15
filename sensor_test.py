from stepper_motor import step_motor
from machine import ADC, Pin
import asyncio

# Open file to log sensor readings
file = open("sensor_test_output.txt", "w")



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
wheelbase_cir = 770
angle = 180
cir = 267
microsteps = 8

# Calculate steps needed for the desired rotation
steps = int((wheelbase_cir/cir)*microsteps * 200 * (angle/360))

for _ in range(steps):
    # Perform steps in forward direction
    motor1.step()
    motor2.step()

    # Log sensor readings
    file.write(str(sensor.read_u16()))
    file.write("\n") 

# Release motors after operation
motor1.release()
motor2.release()

# Change direction for reverse rotation
motor1.set_direction(-1)
motor2.set_direction(-1)

for _ in range(steps):
    # Perform steps in reverse direction
    motor1.step()
    motor2.step()
    
    # Log sensor readings
    file.write(str(sensor.read_u16()))
    file.write("\n") 

# Release motors after operation
motor1.release()
motor2.release()

# Close the log file
file.close()