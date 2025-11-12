from machine import Pin, ADC
import time



class Joystick: 
    def __init__(self, x_pin, y_pin, moter1, moter2, tolerance=5000, middle_value=50000):
        self.x_axis = ADC(Pin(x_pin))
        self.y_axis = ADC(Pin(y_pin))
        self.tolerance = tolerance
        self.middle_value = middle_value
        self.moter1 = moter1
        self.moter2 = moter2
        # Motor speed control variables for speed adjustment
        self.min_pwm = 10
        # Starting speed
        self.current_pwm = self.min_pwm  
        # Max speed     
        self.max_pwm = 20 
        # Speed increment           
        self.pwm_step = 5             
        self.cooldown_delay = 2  
        # Seconds before slowing down     
        self.last_press_time = time.time()

    # Calibrate the joystick to find the center position
    def calibrate(self):
        print("Calibrating... Please leave the joystick centered.")
        time.sleep(2)
        self.middle_value = (self.x_axis.read_u16() + self.y_axis.read_u16()) // 2
        print(f"Calibration complete. New middle value: {self.middle_value}")

    # Read the joystick values
    def read_values(self):
        x_value = self.x_axis.read_u16()
        y_value = self.y_axis.read_u16()
        return x_value, y_value

    # Determine the direction based on joystick position
    def direction(self):
        # Ignore movement detection if button is pressed
        if self.is_button_pressed():
            direction = "CENTER"
            return direction
        
        x_value, y_value = self.read_values()
        direction = "CENTER"

        if x_value < (self.middle_value - self.tolerance):
            direction = "LEFT"
        elif x_value > (self.middle_value + self.tolerance) and x_value < 65000:
            direction = "RIGHT"
        elif y_value < (self.middle_value - self.tolerance):
            direction = "FORWARDS"
        elif y_value > (self.middle_value + self.tolerance):
            direction = "BACKWARDS"
        return direction

    # Check if the button is pressed
    def is_button_pressed(self):
        x_value, _ = self.read_values()
         # Adjust threshold if needed
        return x_value >= 65000 

    # Control the motors based on joystick direction
    def control_motors(self):
        direction = self.direction()
        if direction == "FORWARDS":
            self.moter1.set_direction(1)
            self.moter2.set_direction(1)
            self.moter1.step()
            self.moter2.step()
        elif direction == "BACKWARDS":
            self.moter1.set_direction(-1)
            self.moter2.set_direction(-1)
            self.moter1.step()
            self.moter2.step()
        elif direction == "LEFT":
            self.moter1.set_direction(-1)
            self.moter2.set_direction(1)
            self.moter1.step()
            self.moter2.step()
        elif direction == "RIGHT":
            self.moter1.set_direction(1)
            self.moter2.set_direction(-1)
            self.moter1.step()
            self.moter2.step()
        elif direction == "CENTER":
            self.moter1.release()
            self.moter2.release()

    def adjust_speed(self):
        now = time.time()
        direction = self.direction()

        # Only increase speed if joystick is pressed AND robot is moving
        if self.is_button_pressed() and direction != "CENTER":
            self.last_press_time = now
            if self.current_pwm < self.max_pwm:
                self.current_pwm += self.pwm_step
                print(f"Increasing speed to {self.current_pwm}%")
        else:
            # Only reduce speed if cooldown has passed
            if now - self.last_press_time > self.cooldown_delay:
                if self.current_pwm > self.min_pwm:
                    self.current_pwm -= self.pwm_step
                    print(f"Reducing speed to {self.current_pwm}%")

        # Clamp PWM to stay within min and max bounds
        self.current_pwm = max(self.min_pwm, min(self.current_pwm, self.max_pwm))

        # Apply the PWM to both motors
        self.moter1.set_PWM(self.current_pwm)
        self.moter2.set_PWM(self.current_pwm)

  
