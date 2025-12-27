from machine import UART, Pin, PWM
from time import sleep, time

#Class datacommunication
class DataCom: 
    def __init__(self, tx_pin, rx_pin, baudrate=9600):
        self.uart = UART(0, baudrate=baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin))

    def calibrate_datacomPanza(self, timeout=10):
        start_time = time()

        while time() - start_time < timeout:
            # Send calibration command
            message = "CALIBRATE"
            self.uart.write(message)
            print("Sent:", message)

            # Wait for response
            wait_start = time()
            while time() - wait_start < 1:
                if self.uart.any():
                    data = self.uart.read(20)
                    if data:
                        print("Received:", data.decode().strip())
                        return True
                sleep(0.05)

        print("Calibration timeout")
        return False
        

    def calibrate_datacomPractice(self, timeout=10):
        start_time = time()

        while time() - start_time < timeout:
            if self.uart.any():
                data = self.uart.read(20)
                if data:
                    message = data.decode().strip()
                    print("Received:", message)

                    if message == "CALIBRATE":
                        # Respond
                        response = "CALIBRATED"
                        self.uart.write(response)
                        print("Sent:", response)
                        return True
            sleep(0.05)

        print("No calibration request received")
        return False
                    
                    
    def send_data(self, message):
        self.uart.write(message)
    
    def receive_data(self):
        if self.uart.any():
            data = self.uart.read(20)
            if data:
                return data.decode('utf-8')
        return None
    
    def wait_for_message(self, expected_msg, timeout=10):
        """
        Waits until expected_msg is received or timeout expires.
        Returns True if message received, False if timeout.
        """
        start = time()
        while time() - start < timeout:
            data = self.receive_data()
            if data and data.strip() == expected_msg:  # exact match
                return True
            sleep(0.05)
        return False