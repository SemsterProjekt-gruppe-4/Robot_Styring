# Idea for have to navigate logistic parts of a project

# imports
from machine import Pin, ADC
from stepper_motor import step_motor
from diff_drive import diffdrive
from line_follower import line_follower
from sensor_class import sensor
import time
# mabye need a class for induction sensor

# defines motors and sensors

motor_left =step_motor(0,1,2,3)
motor_right=step_motor(4,5,6,7)
sensors = sensor(26,12,13,14)
linefollower = line_follower(motor_left, motor_right, sensors)
diffdrive = diffdrive(motor_left, motor_right, 267)
induction_sensor_left = ADC(27)
induction_sensor_right = ADC(28)
magnet = Pin(11, Pin.OUT)

# define variables
section = 1
pickups_done = 0

# lengtgs in mm to be changed based on the track design
topoint = 100  # distance to the pickup point from the turn in mm
reverse = 50  # distance to reverse before turning in mm
forward = 150  # distance to drive forward after pickup in mm

# define functions for pickups
def left_prickup():
    # stop line following
    diffdrive.stop()

    # inform the arm to pick up
    # lower arm

    # reverse a bit
    diffdrive.drive(reverse, -1)
    
    # turn left about 170 degrees
    diffdrive.turn(170, "left")

    # drive reverse to the pickup point
    diffdrive.drive(topoint, -1)

    # wait to know the arm is down
    # IDK

    # activate magnet
    # magnet.value(1)

    # wikkle a bit to make sure the object is secure
    diffdrive.turn(5, "right")
    diffdrive.turn(10, "left")
    diffdrive.turn(5, "right")

    # inform arm to lift
    # lift arm

    # drive forward to the turn point
    diffdrive.drive(topoint)

    # turn right to face the line
    diffdrive.turn(170, "right")

    # wait to know the arm is up
    # IDK

    # deavtivate magnet
    # magnet.value(0)

    # drive forward past pickup point to reengage line following
    diffdrive.drive(forward)


def right_prickup():
    # stop line following
    diffdrive.stop()

    # inform the arm to pick up
    # lower arm

    # reverse a bit
    diffdrive.drive(reverse, -1)
    
    # turn right about 170 degrees
    diffdrive.turn(170, "right")

    # drive reverse to the pickup point
    diffdrive.drive(topoint, -1)

    # wait to know the arm is down
    # IDK

    # activate magnet
    # magnet.value(1)

    # wikkle a bit to make sure the object is secure
    diffdrive.turn(5, "right")
    diffdrive.turn(10, "left")
    diffdrive.turn(5, "right")

    # inform arm to lift
    # lift arm

    # drive forward to the turn point
    diffdrive.drive(topoint)

    # turn left to face the line
    diffdrive.turn(170, "left")

    # wait to know the arm is up
    # IDK

    # deavtivate magnet
    # magnet.value(0)

    # drive forward past pickup point to reengage line following
    diffdrive.drive(forward)

# sperate the track into sections
# section 1 is the start  with the two first pickups
# section 2 is the right branch with x pickups
# section 3 is the left branch with x pickups
# section 4 is the final straight to the end with the last pickups


while True:
    while section == 1:
        sensor_data = sensor.read_sensor_data(1.7)
        linefollower.drive(sensor_data)
        if sensor_data[0] == 1 and pickups_done < 2:
            # left prickup detected
            left_prickup()
            pickups_done += 1
        if sensor_data[7] == 1 and pickups_done < 2:
            # right pickup detected
            right_prickup()
            pickups_done += 1
        if pickups_done >= 2 and sensor_data[7] == 1:
            # end of section 1 detected
            diffdrive.drive(50)  # drive forward a bit to clear the turn
            diffdrive.turn(90, "right")  # turn right to the right branch
            diffdrive.drive(50)  # drive forward to reengage line following
            section = 2
            break
    while section == 2:
        sensor_data = sensor.read_sensor_data(1.7)
        linefollower.drive(sensor_data)
        # similar logic for pickups and section transitions
        # ...
        # when done with section 2
        # section = 3
        break


