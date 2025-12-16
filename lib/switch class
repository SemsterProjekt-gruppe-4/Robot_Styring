import machine, utime

class SPDT_Switch:
    def __init__(self, pin_botten, active_high=True, debounce_ms=25):

        self.pin = machine.Pin(pin_botten, machine.Pin.IN, machine.Pin.PULL_DOWN if active_high else machine.Pin.PULL_UP)
        self.active_high = active_high
        self.debounce_ms = debounce_ms
        self._last_state = self.pin.value()
        self._stable_state = self._last_state
        self._last_change = utime.ticks_ms()

    def update(self):
        current = self.pin.value()
        now = utime.ticks_ms()
        if current != self._last_state:
            self._last_change = now
            self._last_state = current
        if utime.ticks_diff(now, self._last_change) >= self.debounce_ms:
            self._stable_state = self._last_state

    def is_pressed(self):
        self.update()
        if self.active_high:
            return self._stable_state == 1
        else:
            return self._stable_state == 0
        
# Example
switch = SPDT_Switch(pin_botten=14, active_high=True)

while True:
    if switch.is_pressed():
        print("Pressed")
    else:
        print("Released")
    utime.sleep_ms(100)
