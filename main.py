from sensor import sensor
from test import linefollower
from stepper import step_motor

motorR = step_motor(0,1,2,3)
motorL = step_motor(4,5,6,7)

# sets microsteps to 8 and PWM = 20%
motorR.set_microsteps(8,20)
motorL.set_microsteps(8,20)

sensor = sensor(26,12,13,14)

linefollower = linefollower(sensor, motorL, motorR)

while True:
    linefollower.drive()
