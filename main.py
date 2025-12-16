from sensor_class import sensor
from line_follower import linefollower
from stepper_class import step_motor

# Initialize motors
motorR = step_motor(0,1,2,3)
motorL = step_motor(4,5,6,7)

# sets fullsteps and PWM = 65%
motorR.set_microsteps(1, 65)
motorL.set_microsteps(1, 65)

# Initialize sensor
sensor = sensor(26,12,13,14, 1.7)

# Initialize the linefollower class
linefollower = linefollower(sensor, motorL, motorR)

while True:
    # drives the robot
    linefollower.drive()
