#listener message
from machine import Pin, ADC, PWM
from stepper_motor import step_motor
import network
import socket
import time
import _thread

INTERNET_Name = "Bosssebastian's Phone"
INTERNET_PASSWORD = "123456789"

led = PWM(8, freq=1000)
delay = 0.001

moter1 = step_motor(0,1,2,3)
moter2 = step_motor(4,5,6,7)

moter1.set_PWM(30)
moter2.set_PWM(30)

moter1.set_microsteps(12)
moter2.set_microsteps(12)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(INTERNET_Name, INTERNET_PASSWORD)

max_wait = 10
while max_wait>0:
    if wlan.status()< 0 or wlan.status()>=3:
        break
    max_wait -= 1        
    print('waiting for connection')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip='+status[0])
    
addr = socket.getaddrinfo ('10.179.176.63', 80)[0][-1]

s=socket.socket()
s.connect(addr)

print('listening on', addr)
direction = None
def drive():
    t = True
    global direction, delay
    while t:
        try:
            time.sleep(delay)
            if direction == "FORWARDS":
                moter1.set_direction(1)
                moter2.set_direction(1)
                moter1.step()
                moter2.step()
                moter1.release()
                moter2.release()
            elif direction == "BACKWARDS":
                moter1.set_direction(-1)
                moter2.set_direction(-1)
                moter1.step()
                moter2.step()
                moter1.release()
                moter2.release()
            elif direction == "LEFT":
                moter1.set_direction(1)
                moter2.set_direction(-1)
                moter1.step()
                moter2.step()
                moter1.release()
                moter2.release()
            elif direction == "RIGHT":
                moter1.set_direction(-1)
                moter2.set_direction(1)
                moter1.step()
                moter2.step()
                moter1.release()
                moter2.release()
            elif direction == "stop":
                moter1.release()
                moter2.release()
                t = False
                break
            else:
                moter1.release()
                moter2.release()
        except:
            moter1.release()
            moter2.release()
        


_thread.start_new_thread(drive, ())
while True:
    try:
        try:
            direction, delay = s.recv(1024).decode().split(',')
            delay = 0.005 - (65535 - int(delay)) / 65535 * 0.000999 * 5
            led.duty_u16(int(65535 * (1-10*delay)))
        except ValueError:
            pass
    except OSError as e:
        direction = "stop"

