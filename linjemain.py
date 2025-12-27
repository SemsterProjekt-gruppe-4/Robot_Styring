#main.py
from machine import UART, Pin, PWM
from stepper_motor import step_motor
from time import sleep
from sensor import sensor
from insensor import insensor
from DataCom import DataCom
from line_follower_class import linefollower
from diffdrive import diffdrive
from math import cos, pi


# Initialize UART for communication
#uart = DataCom(tx_pin=12, rx_pin=13) 

# Initialize motors
motorR = step_motor(0,1,2,3) #grønt hjul
motorL = step_motor(4,5,6,7) #hvidt hjul

# sets microsteps to 8 and PWM = 20%
motorR.set_microsteps(8, 40)
motorL.set_microsteps(8, 40)

#electromagnet
electromagnet = PWM(Pin(8))
electromagnet.freq(4000)
electromagnet.duty_u16(0) 

print(1)

# Initialize sensor
sensor = sensor(26,14,15,18)

#initialize induction sensor
insensor = insensor(9)

# Initialize the linefollower class
linefollower = linefollower(sensor, motorL, motorR)

circumfrense=int(140*pi)
wheelbase=int(210*pi)

diffdrive = diffdrive(motorR, motorL, circumfrense, 8, wheelbase)

print(2)

sleep(1)

#uart.calibrate_datacomPanza()

print(3)

test = 0
#nut_count = 0
# drives the robot
while True: 
    linefollower.drive()
    sensor_data = sensor.read_sensor_data(1.7)
    if sensor_data[1] == 1 and sensor_data[6] == 1:
        for _ in range(2550):
            motorL.step()
            motorR.step()
            sleep(0.001)
        sleep(0.2)
        twerk_timer = 0
        electromagnet.duty_u16(40000)
        while twerk_timer <= 5:
            diffdrive.turn(15, 'right') 
            sleep(0.5)
            diffdrive.turn(15, 'left')
            twerk_timer += 1
            motorR.release()
            motorL.release()
        motorL.set_direction(-1)
        for _ in range(135 * 8):
            motorL.step()
            motorR.step()
            sleep(0.001)
        sleep(0.2)
        motorL.set_direction(1)
        for _ in range(2300):
            motorL.step()
            motorR.step()
            sleep(0.001)


#diffdrive.turn(180, 'right')
#diffdrive.drive(200,1)
#linefollower.drive()



