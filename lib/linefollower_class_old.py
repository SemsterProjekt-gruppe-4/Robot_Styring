class linefollower:
    def __init__(self, moter1, moter2, robot):
        self.sensor_weights = [-8, -4, -2, -1, 1, 2, 4, 8]
        self.sensor_cutoff = 1.7
        self.tolerance = 15
        self.max_turn_angle = 45
        
        # initialize variables
        self.turn_angle = 0
        self.direction = "straight"

        # motors
        self.moter1 = moter1
        self.moter2 = moter2

        self.moter1.set_PWM(20)
        self.moter2.set_PWM(20)

        self.robot = robot


    def calculate_turn_angle(self, sensor_data):
        total = 0

        for i in range(8):
            total += sensor_data[i] * self.sensor_weights[i]

        sum_data = sum(sensor_data)

        # No sensors triggered
        if sum_data == 0:
            self.direction = "lost"
            self.turn_angle = 0
            return 0, "lost"

        # Normalize and scale
        self.turn_angle = (total / 12) * self.max_turn_angle

        # Apply tolerance
        if abs(self.turn_angle) > self.tolerance:
            if self.turn_angle > 0:
                self.direction = "left"
            else:
                self.direction = "right"
        else:
            self.direction = "straight"
            self.turn_angle = 0

        print("turn angle:", self.turn_angle)
        print("direction:", self.direction)

        return self.turn_angle, self.direction
    

    def follow_line(self, sensor_obj):
        """Reads sensors, calculates turn, then drives."""
        
        sensor_data = sensor_obj.read_sensor_data(self.sensor_cutoff)
        turn_angle, direction = self.calculate_turn_angle(sensor_data)

        if direction == "straight":
            self.robot.drive(10)
        else:
            self.robot.turn_one_wheel(turn_angle, direction)
