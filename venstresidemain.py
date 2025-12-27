#main.py
from machine import UART, Pin, PWM
from stepper_motor import step_motor
from time import sleep
from sensor import sensor
from insensor import insensor
from DataCom import DataCom
from line_follower_class_left import linefollower
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
nut_count = 0
# drives the robot
sleep(2)
diffdrive.drive(2270,1)
motorR.release()
motorL.release()
diffdrive.turn(90, 'right')
#sleep(1)
while True: 
    linefollower.drive() 
    if insensor.read() == 1:
        nut_count += 1
        print(6)
        diffdrive.drive(160, dir=1)
        print(4)
        motorR.release()
        motorL.release()
        diffdrive.turn(100, 'right')
        print
        sleep(1)
        
        diffdrive.drive(90, dir=1)

        motorR.release()
        motorL.release()
        

# Send "reached destination" message and wait for acknowledgment
        #uart.send_data('reached destination')
        #print('send', 'reached destination')
        #if uart.wait_for_message('arm down', timeout=20):
            #print('Arm down acknowledged')
        
        
        sleep(0.2)
        twerk_timer = 0
        electromagnet.duty_u16(40000)
        while twerk_timer <= 5:
            diffdrive.turn(10, 'left') 
            sleep(0.5)
            diffdrive.turn(10, 'right')
            twerk_timer += 1
            motorR.release()
            motorL.release()
            
        diffdrive.drive(140, dir=-1)
            
        motorR.release()
        motorL.release()
        
         # Send "done twerking" message and wait for acknowledgment
        #uart.send_data('done twerking')
        #print('send', 'done twerking')
        #if uart.wait_for_message('arm up', timeout=20):
            #print('Arm up acknowledged')

        diffdrive.turn(80, 'left')
        motorR.release()
        motorL.release()
        
        if nut_count == 2:
            diffdrive.turn(45, 'left')
            diffdrive.drive(500, dir=1)
                
                
                
                
