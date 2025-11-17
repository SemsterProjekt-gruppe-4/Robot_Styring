# read sensors
from machine import Pin, ADC
import time
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
p1 = Pin(14, Pin.OUT)
p2 = Pin(13, Pin.OUT)
p3 = Pin(12, Pin.OUT)
li = ADC(26)
sensor_data = [0,0,0,0,0,0,0,0]



while True:
    for i in range(8):
        p3.value(sensor_seq[i][0])
        p2.value(sensor_seq[i][1])
        p1.value(sensor_seq[i][2])
        time.sleep(0.05)
        sensor_data[i] = li.read_u16()
        
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