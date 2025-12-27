#insensor class
from machine import Pin
import time

class insensor:
    def __init__(self, Pin1):
        self.ic1_pin = Pin(Pin1, Pin.IN)
        
    def read(self):
        return (self.ic1_pin.value())