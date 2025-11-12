# read sensors
from machine import Pin, ADC
# greycode to step throgh all sensors
sensor_seq=[
    [0,0,0],
    [0,0,1],
    [0,1,1],
    [0,1,0],
    [1,1,0],
    [1,1,1],
    [1,0,1],
    [1,0,0]
]
pins = [Pin(12, Pin.OUT), Pin(13, Pin.OUT), Pin(14, Pin.OUT)]
li = ADC(0)
sensor_data = [0,0,0,0,0,0,0,0]

while True:
    for i in range(8):
        for pin in pins:
            pins[pin] = sensor_seq[i][pin]
        sensor_data[i] = (li.read_u16() * 3.3 /65536)
    print(sensor_data)    

'''
# calculate how much to turn
sensor_weights = [-8, -4, -2, -1, 1, 2, 4, 8]
total = 0
for i in range(8):
    total += sensor_data[i] * sensor_weights[i]
turn = total / sum(sensor_data) * max_turn_angle
return turn

'''