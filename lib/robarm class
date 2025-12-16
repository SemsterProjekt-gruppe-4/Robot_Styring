
class RobArm:
    def __init__(self, motor, SPDTDOWN, SPDTUP, elektromagnet):
        self.motor = motor
        self.SPDTDOWN = SPDTDOWN
        self.SPDTUP = SPDTUP
        self.electromagnet = elektromagnet

    def armDOWN(self):
        self.motor.Set_direction(1)

        while not self.SPDTDOWN.is_pressed():
            self.motor.step()

        if self.SPDTDOWN.is_pressed():
            self.motor.release()
            
            self.elektromagnet.value(1)

    def armUP(self):
        self.motor.Set_direction(-1)

        while not self.SPDTUP.is_pressed():
            self.motor.step()

        if self.SPDTUP.is_pressed():
            self.motor.release()
            sleep(1)
            self.elektromagnet.value(0)

