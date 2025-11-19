class sensor: 
    def __init__(self, ADC_input, s0, s1, s2):
        self.ADC = ADC(Pin(ADC_input))
        self.s0 = Pin(s0, Pin.OUT)
        self.s1 = Pin(s1, Pin.OUT)
        self.s2 = Pin(s2, Pin.OUT)

        self.sensor_data = [0] * 8

        self.sensor_seq = [
            [0,0,0],
            [0,0,1],
            [0,1,1],
            [0,1,0],
            [1,1,0],
            [1,1,1],
            [1,0,1],
            [1,0,0]
        ]

    def read_sensor_data(self, sensor_cutoff):
        for i in range(len(self.sensor_seq)):

            self.s2.value(self.sensor_seq[i][0])
            self.s1.value(self.sensor_seq[i][1])
            self.s0.value(self.sensor_seq[i][2])

            time.sleep(0.05)

            voltage = self.ADC.read_u16() * 3.3 / 65536

            if voltage < sensor_cutoff:
                self.sensor_data[i] = 1
            else:
                self.sensor_data[i] = 0

        return self.sensor_data

