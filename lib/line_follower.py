# line_follower Rullemarie
class linefollower:
    def __init__(self, sensor_obj, motorleft, motorright):
        '''sensor_obj, motorleft, motorright'''
        self.sensor = sensor_obj
        self.motorleft = motorleft
        self.motorright = motorright
        self.right_steps = 0
        self.left_steps = 0


    def follow_line(self,sensor_data):
        # resets variables
        right_step = 0
        left_step = 0
        total_step = 0

        if sensor_data[1] == 1:
            right_step += 1
            left_step += 0.2
            total_step += 1
            #print("Left outer mid sensor triggered")
        if sensor_data[2] == 1:
            right_step += 1
            left_step += 0.6
            total_step += 1
            #print("Left inner mid sensor triggered")
        if sensor_data[3] == 1:
            right_step += 1
            left_step += 1
            total_step += 1
            #print("Left inner sensor triggered")
        if sensor_data[4] == 1:
            right_step += 1
            left_step += 1
            total_step += 1
            #print("Right inner sensor triggered")
        if sensor_data[5] == 1:
            right_step += 0.6
            left_step += 1
            total_step += 1
            #print("Right inner mid sensor triggered")
        if sensor_data[6] == 1:
            right_step += 0.2
            left_step += 1
            total_step += 1
            #print("Right outer mid sensor triggered")
        if total_step == 0:
            #print("No sensors triggered: Lost line")
            self.motorleft.release()
            self.motorright.release()
            return 0
            
        self.right_steps += (right_step / total_step)
        self.left_steps += (left_step / total_step)
        #print(f"Calculated steps - Right: {self.right_steps}, Left: {self.left_steps}")
        
    def drive(self):
        self.follow_line()
        if self.right_steps > 1:
            self.right_steps -= 1
            self.motorright.set_direction(1)
            self.motorright.step()
        if self.left_steps > 1:
            self.left_steps -= 1
            self.motorleft.set_direction(1)
            self.motorleft.step()
            '''
        if self.right_steps < -1:
            self.right_steps += 1
            self.motorright.set_direction(-1)
            self.motorright.step()
        if self.left_steps < -1:
            self.left_steps += 1
            self.motorleft.set_direction(-1)
            self.motorleft.step()
            '''

        
        