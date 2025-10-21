from machine import PWM
from math import cos, pi

class step_motor:
    def __init__(self, pin1, pin2, pin3, pin4):
        '''
        Motor Pin 1-4, 
        '''
        # Initialize PWM on motor control pins
        self.pwm1 = PWM(pin1, freq=18000)
        self.pwm2 = PWM(pin2, freq=18000)
        self.pwm3 = PWM(pin3, freq=18000)
        self.pwm4 = PWM(pin4, freq=18000)

        # Max duty cycle for 16-bit PWM
        self.duty = 65535  

        # Define the step sequence for a 4-step motor (full step)
        self.step_sequence = [
            [int(self.duty*0.5), 0, 0, 0],
            [0, int(self.duty*0.5), 0, 0],
            [0, 0, int(self.duty*0.5), 0],
            [0, 0, 0, int(self.duty*0.5)]
        ]
        # Current position in the step sequence
        self.current_step = 0
        self.current_microstep = 0
        self.direction = 1 # forwards = 1 and backwards = -1

    def release(self):
        '''releases motor "to save power and prevent overheating"'''
        self.pwm1.duty_u16(0)
        self.pwm2.duty_u16(0)
        self.pwm3.duty_u16(0)
        self.pwm4.duty_u16(0)

    def set_direction(self, direction):
        '''
        sets the direction of the motor\n
        direction = 1 for forwards, -1 for backwards 
        '''
        # validate input
        if direction != 1 and direction != -1:
            raise ValueError("Direction must be either 1 or -1")
        # set direction
        self.direction = direction
        
    def set_PWM(self, PWM):
        '''sets the PWM duty cycle (0-100%)'''
        # validate input
        if PWM < 0 or PWM > 100:
            raise ValueError("PWM must be between 0 and 100")
        # set duty cycle
        self.duty = int(PWM / 100 * 65535)

    def set_microsteps(self, microsteps):
        ''' generates a new step sequence for the given number of microsteps'''
        # validate input
        # must be a positive integer
        if microsteps < 1:
            raise ValueError("Microsteps must be at least 1")
        
        # 1 = full step, 2 = half step, 4 = quarter step, 8 = eighth step etc'''

        #generate new step sequence for microstepping
        # clear existing sequence
        self.step_sequence = []
        # generate new sequence (microsteps per full step * number of full steps (4))
        for i in range(microsteps*4):
            # calculate the sine wave values for each coil
            # angle ranges from 0 to 2*pi over the full step sequence
            angle = (i / microsteps) * (pi / 2)  # Calculate the angle for the sine wave

            # calculate the PWM duty cycle for each coil using a sine wave
            # cos(angle - phase shift) to get the correct phase for each coil
            # max(0, ...) to ensure no negative duty cycles
            step = [
                max(0,round(cos(angle - 0 * (pi / 2)))),
                max(0,round(cos(angle - 1 * (pi / 2)))),
                max(0,round(cos(angle - 2 * (pi / 2)))),
                max(0,round(cos(angle - 3 * (pi / 2))))
            ]
            # append the calculated step to the step sequence
            self.step_sequence.append(step)

    def step(self):
        '''step the motor in the given direction by one step in the step sequence'''
        # get the current step from the sequence
        step = self.step_sequence[self.current_step]
        # set the PWM duty cycle for each coil
        self.pwm1.duty_u16(int(step[0] * self.duty))
        self.pwm2.duty_u16(int(step[1] * self.duty))
        self.pwm3.duty_u16(int(step[2] * self.duty))
        self.pwm4.duty_u16(int(step[3] * self.duty))
        # update the current step based on the direction
        if self.direction == -1:
            self.current_step = (self.current_step - 1) % len(self.step_sequence)
        else:
            self.current_step = (self.current_step + 1) % len(self.step_sequence)

