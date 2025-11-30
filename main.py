#listener message
from machine import Pin, ADC, PWM
from stepper_motor import step_motor
import network
import socket
import time
import _thread

# WiFi Credentials
INTERNET_Name = "Bosssebastian's Phone"
INTERNET_PASSWORD = "123456789"

# IP address of the server (has to be changed to the server's IP)
IP = "10.179.176.129"

# Set default delay
delay = 0.001

# Initialize motors
moter1 = step_motor(0,1,2,3)
moter2 = step_motor(4,5,6,7)

# Set motor parameters
# Ser motors Max PWM
moter1.set_PWM(30)
moter2.set_PWM(30)
# Set motors microsteps
moter1.set_microsteps(12)
moter2.set_microsteps(12)

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(INTERNET_Name, INTERNET_PASSWORD)

# Wait for connection with timeout
max_wait = 10
while max_wait>0:
    # Check if connected to the WiFi or failed
    if wlan.status()< 0 or wlan.status()>=3:
        # Connection successful or failed
        break
    # Wait a second and decrement max_wait
    max_wait -= 1        
    print('waiting for connection')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')

# else successful connection
print('connected')

# set the IP address fir the server
addr = socket.getaddrinfo (IP, 80)[0][-1]

# create socket and connect to server
s=socket.socket()
s.connect(addr)

# Start listening for commands
print('listening on', addr)
direction = None
# Drive function
def drive():
    t = True
    global direction, delay
    while t:
        try:
            # Pause for the specified delay
            time.sleep(delay)
            # Read direction and move motors accordingly
            if direction == "FORWARDS":
                moter1.set_direction(1)
                moter2.set_direction(1)
                moter1.step()
                moter2.step()
            elif direction == "BACKWARDS":
                moter1.set_direction(-1)
                moter2.set_direction(-1)
                moter1.step()
                moter2.step()
            elif direction == "LEFT":
                moter1.set_direction(1)
                moter2.set_direction(-1)
                moter1.step()
                moter2.step()
            elif direction == "RIGHT":
                moter1.set_direction(-1)
                moter2.set_direction(1)
                moter1.step()
                moter2.step()
            # Stop condition
            elif direction == "stop":
                t = False
                break
        except:
            pass

        # Release motors to prevent overheating
        moter1.release()
        moter2.release()
           
        

# Start drive function in a "new thread" morelike asyncrionously
_thread.start_new_thread(drive, ())

# Main loop to receive commands
while True:
    try:
        try:
            # Receive direction and delay from the socket
            direction, delay = s.recv(1024).decode().split(',')
            delay = 0.005 - (65535 - int(delay)) / 65535 * 0.000999 * 5
        except ValueError:
            pass
    except OSError as e:
        # Handle socket error
        direction = "stop"

