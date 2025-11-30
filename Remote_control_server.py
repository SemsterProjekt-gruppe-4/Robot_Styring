from machine import Pin, ADC, I2C
from joystick import Joystick 
from ssd1306 import SSD1306_I2C
import network
import socket
import time

# WiFi connection details
INTERNET_Name = "Bosssebastian's Phone"
INTERNET_PASSWORD = "123456789" 

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(INTERNET_Name, INTERNET_PASSWORD)

# Wait for connection with timeout
max_wait = 20
while max_wait>0:
    if wlan.isconnected():
        break
    max_wait -= 1        
    print('waiting for connection')
    time.sleep(0.5)

# Check if connected
if not wlan.isconnected():
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip='+status[0])
    
# Setup socket server
addr = socket.getaddrinfo ('0.0.0.0', 80)[0][-1]
server=socket.socket()
server.bind(addr)
server.listen(1)
print ('listening on', addr)

# Setup joystick and potentiometer
joystick = Joystick(26, 27)
joystick.calibrate()
pot = ADC(Pin(28))

# Extra 3.3 output pin
pin1 = Pin(2); pin1.value(1)

# Setup pins and I2C
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = SSD1306_I2C(128, 64, i2c)
oledCounter = 9


while True:
    try:
        # Wait for a client to connect
        print('Waiting for client to connect...')
        cl, client_addr = server.accept()
        print('Client connected from', client_addr)

        while True:
            try:
                # Read joystick direction and potentiometer value
                direction = joystick.direction()
                delay = pot.read_u16()

                # Send direction and speed to client
                message = (direction + "," + str(delay))

                cl.send(message)
                print(message)
                # Update OLED display every 10 loops
                oledCounter += 1

                if oledCounter >= 10:
                    oledCounter = 0

                    # Determine speed text based on potentiometer value
                    if delay < 21845:
                        speedText = "Fast"
                    elif delay < 43690:
                        speedText = "Medium"
                    else:
                        speedText = "Slow"
                    
                    # Update OLED display
                    oled.fill(0)
                    oled.text("Direction:", 0, 0)
                    oled.text(direction, 0, 15)
                    oled.text("Speed:", 0, 30)
                    oled.text(speedText, 0, 45)
                    oled.show()
                # Short delay before next loop
                time.sleep(0.3)
            
            # Handle client disconnection
            except OSError:
                print('Client disconnected')
                cl.close()
                break

    # Handle server shutdown
    except KeyboardInterrupt:
        print("Server closed.")
        server.close()
        break
 