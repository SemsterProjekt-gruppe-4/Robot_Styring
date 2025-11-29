from machine import Pin, ADC
import time

class Joystick:
    def __init__(self, x_pin, y_pin, tolerance=5000, middle_value=32767):
        # Initialize joystick axes
        self.x_axis = ADC(Pin(x_pin))
        self.y_axis = ADC(Pin(y_pin))
        # set parameters
        self.tolerance = tolerance
        self.middle_value = middle_value

        
    def calibrate(self):
        '''Calibrate the joystick to find the middle value.'''
        print("Calibrating... Leave joystick centered.")
        # Wait for user to center joystick
        time.sleep(2)
        # Read current values and set that as the middle
        voltagex, voltagey = self.read_values()
        self.middle_value = int((voltagex + voltagey) / 2)
        print(f"Calibration complete. Middle value: {self.middle_value}")

    def read_values(self):
        '''Read the current voltage values from the joystick axes.'''
        return self.x_axis.read_u16(), self.y_axis.read_u16()

    def direction(self):
        '''Determine the direction of the joystick.'''
        voltagex, voltagey = self.read_values()
        # Determine direction based on voltage readings and tolerance
        if voltagex < (self.middle_value - self.tolerance):
            return "LEFT"
        elif voltagex > (self.middle_value + self.tolerance):
            return "RIGHT"
        elif voltagey < (self.middle_value - self.tolerance):
            return "FORWARDS"
        elif voltagey > (self.middle_value + self.tolerance):
            return "BACKWARDS"
        return "CENTER"
