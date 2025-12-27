# Insert the class for your final version of the Differential Drive class
import time

class diffdrive:
    def __init__(self, motor1: step_motor, motor2: step_motor, cir, microsteps, wheelbase):
        # Initialize the differential drive with two stepper motors, wheel circumference, and microsteps
        self.motor1 = motor1
        self.motor2 = motor2
        
        # set microsteps for both motors
        self.motor1.set_microsteps(microsteps)
        self.motor2.set_microsteps(microsteps)
        # store microsteps
        self.microsteps = microsteps
        
        # default values for the robot
        # wheelbase circumference in mm
        self.wheelbase_cir = wheelbase
        
        # wheel circumference in mm
        self.cir = cir

    def drive (self, length, dir=1):
        '''drive motor a given length in mm'''
        # Length / (circumference * steps per rev * microsteps) = number of microsteps to move
        steps = int((length/self.cir)* self.microsteps * 200) # calculate number of microsteps to move
        
        if dir == -1:
            #sets the direction of the motors to backwards
            self.motor1.set_direction(-1)
            self.motor2.set_direction(-1)
        else:
            #sets the direction of the motors to forwards
            self.motor1.set_direction(1)
            self.motor2.set_direction(1)
        
        #steps the motors the calculated number of steps
        for _ in range(steps):
            self.motor1.step()
            self.motor2.step()
            time.sleep(0.001)
            
    def turn (self, angle,dir):
        '''turns given angle'''
        # (wheelbase_cir/wheel_cir) * steps per rotation * (given angle/360)
        
        steps = int((self.wheelbase_cir/self.cir)*self.microsteps * 200 * (angle/360))
        
        print(steps)
        # sets the direction of the motors based on the turn direction
        # one motor forwards, one backwards
        # which motor goes which way depends on the turn direction and the how the motors are mounted
        if dir == "right" or dir == "r":
            self.motor1.set_direction(-1)
            self.motor2.set_direction(1)
            
        elif dir == "left" or dir == "l":
            self.motor1.set_direction(1)
            self.motor2.set_direction(-1)
        else:
            raise ValueError('turn direction must either be "right" or "left"')

        #steps the motors the calculated number of steps
        for _ in range(steps):
            self.motor1.step()
            self.motor2.step()
            time.sleep(0.001)
    def turn_one_wheel(self, angle, dir):
        '''turns given angle using only one wheel'''
        # (wheelbase_cir/wheel_cir) * steps per rotation * (given angle/360)
        
        steps = int(((self.wheelbase_cir*2)/self.cir)*self.microsteps * 200 * (angle/360))
        
        # sets the direction of the motors based on the turn direction
        if dir == "right" or dir == "r":
            self.motor1.set_direction(1)

            # steps the motor the calculated number of steps
            for _ in range(steps):
                self.motor1.step()

            
        elif dir == "left" or dir == "l":
            self.motor2.set_direction(1)
            
            # steps the motor the calculated number of steps
            for _ in range(steps):
                self.motor2.step()

        else:
            raise ValueError('turn direction must either be "right" or "left"')