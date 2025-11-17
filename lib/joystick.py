from machine import Pin, ADC
import time

class Joystick:
    def __init__(self, x_pin, y_pin, pot, moter1, moter2, tolerance=5000, middle_value=32767):
        self.x_axis = ADC(Pin(x_pin))
        self.y_axis = ADC(Pin(y_pin))
        self.pot = ADC(Pin(pot))
        self.tolerance = tolerance
        self.middle_value = middle_value
        self.moter1 = moter1
        self.moter2 = moter2
        self.max_speed = 0.2
        self.start_speed = 0.05
        self.current_speed = self.start_speed

    def calibrate(self):
        print("Calibrating... Leave joystick centered.")
        time.sleep(2)
        voltagex, voltagey, _ = self.read_values()
        self.middle_value = int((voltagex + voltagey) / 2)
        print(f"Calibration complete. Middle value: {self.middle_value}")

    def read_values(self):
        return self.x_axis.read_u16(), self.y_axis.read_u16(), self.pot.read_u16()

    def direction(self):
        voltagex, voltagey, _ = self.read_values()
        if voltagex < (self.middle_value - self.tolerance):
            return "LEFT"
        elif voltagex > (self.middle_value + self.tolerance):
            return "RIGHT"
        elif voltagey < (self.middle_value - self.tolerance):
            return "FORWARDS"
        elif voltagey > (self.middle_value + self.tolerance):
            return "BACKWARDS"
        return "CENTER"

    def adjust_speed(self):
        _, _, pot_value = self.read_values()
        pot_value = max(0, min(65535, pot_value))
        if pot_value < 1000:
            self.current_speed = self.start_speed
        else:
            self.current_speed = self.start_speed + (pot_value - 1000) / (65535 - 1000) * (self.max_speed - self.start_speed)
        pwm_percent = self.current_speed * 100
        self.moter1.set_PWM(pwm_percent)
        self.moter2.set_PWM(pwm_percent)
        print(f"Speed adjusted: {pwm_percent:.2f}%")

    def control_motors(self):
        dir = self.direction()
        print(f"Direction: {dir}")
        if dir == "FORWARDS":
            self.moter1.set_direction(1)
            self.moter2.set_direction(1)
            print("Moving FORWARDS")
        elif dir == "BACKWARDS":
            self.moter1.set_direction(-1)
            self.moter2.set_direction(-1)
            print("Moving BACKWARDS")   
        elif dir == "LEFT":
            self.moter1.set_direction(-1)
            self.moter2.set_direction(1)
            print("Moving LEFT")
        elif dir == "RIGHT":
            self.moter1.set_direction(1)
            self.moter2.set_direction(-1)
            print("Moving RIGHT")
        else:
            self.moter1.release()
            self.moter2.release()
            print("Stopping")
            return
        self.moter1.step()
        self.moter2.step()

