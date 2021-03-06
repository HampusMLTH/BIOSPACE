#!/usr/bin/env python3
from time import sleep, strftime
import os
#from picamera import PiCamera
from csv import reader,writer
import brickpi3
import shutil

class GoniometerObject(object):
    """ class for controlling the goniometer"""
    SCATTER = "SCATTER"
    YAW = "YAW"
    ROLL = "ROLL"

    def __init__(self):
        #self.pos_led = 0
        #self.pos_stage = 0
        #self.pos_sample = 0

        self.BP = brickpi3.BrickPi3()
        self.init_motors()

    def test(self):
        print("dab")

    @property
    def scatter_angle(self):
        """get led angle"""
        pos = self.BP.get_motor_encoder(self.BP.PORT_C)
        angle = pos*360/(7*8652)
        return angle


    @scatter_angle.setter
    def scatter_angle(self, angle):
        """Set the led angle"""
        self.BP.set_motor_limits(self.BP.PORT_C, 100, 1440)
        pos1=round(8652*7*(angle/360))
        self.BP.set_motor_position(self.BP.PORT_C, pos1)
        #sleep(abs(round(8652*7*(angle/360)/1440)+1))

    @property
    def yaw_angle(self):
        """get stage angle"""
        pos = self.BP.get_motor_encoder(self.BP.PORT_A)
        angle = pos*360/2700
        return angle

    @yaw_angle.setter
    def yaw_angle(self, angle):
        """Set the stage angle"""
        chk_pos = self.BP.get_motor_encoder(self.BP.PORT_A)
        self.BP.set_motor_limits(self.BP.PORT_A, 100, 100)#1440)
        pos1=round(2700*(angle/360))
        #print("pos1", pos1)
        #print(GoniometerObject.angle_2_motorpos(angle, self.STAGE))
        pos_chk=pos1+0.1
        self.BP.set_motor_position(self.BP.PORT_A, pos1)

        if abs(chk_pos-pos_chk) > 10:
            pos2=-angle
            self.BP.set_motor_limits(self.BP.PORT_B, 100, 100/7.5)#1440/7.5)
            self.BP.set_motor_position(self.BP.PORT_B, pos2)

        #sleep(angle*2/1440+1)

        # move the motor
        #print("moving")
        #print(self.angle_2_motorpos(angle, self.STAGE))

    @property
    def roll_angle(self):
        """get sample angle"""
        pos = self.BP.get_motor_encoder(self.BP.PORT_B)
        angle = pos/2
        return angle

    @roll_angle.setter
    def roll_angle(self, angle):
        """Set the sample angle"""
        self.BP.set_motor_limits(self.BP.PORT_B, 100, 100)#1440)
        pos1=angle*2
        self.BP.set_motor_position(self.BP.PORT_B, pos1)
        #sleep(round(2700*(angle/360))/1440+1)

    @property
    def polarizer_angle(self):
        pos = self.BP.get_motor_encoder(self.BP.PORT_D)
        angle = pos/3.75
        return angle


    @polarizer_angle.setter
    def polarizer_angle(self, angle):
        self.BP.set_motor_limits(self.BP.PORT_D, 100, 100)#1440)
        self.BP.set_motor_position(self.BP.PORT_D, angle*3.75)

    def init_motors(self):
        self.BP.offset_motor_encoder(self.BP.PORT_A, self.BP.get_motor_encoder(self.BP.PORT_A))
        self.BP.offset_motor_encoder(self.BP.PORT_B, self.BP.get_motor_encoder(self.BP.PORT_B))
        self.BP.offset_motor_encoder(self.BP.PORT_C, self.BP.get_motor_encoder(self.BP.PORT_C))
        self.BP.offset_motor_encoder(self.BP.PORT_D, self.BP.get_motor_encoder(self.BP.PORT_D))

    def done_moving(self, motor):
        status_2_steps_back = []
        for i in range(1,120):
            prev_status = self.motor_status(motor)
            sleep(0.05)
            status = self.motor_status(motor)
            #print(status)

            if prev_status == status:
                #print("SAME!")
                break
            elif status_2_steps_back == status:
                #If it jumps between 2 posistions
                #print("stop jumping!")
                self.BP.reset_all()
                break
            status_2_steps_back = prev_status

    def motor_status(self, motor):
        try:
            if motor == GoniometerObject.SCATTER:
                status = self.BP.get_motor_status(self.BP.PORT_C)
            elif motor == GoniometerObject.YAW:
                status = self.BP.get_motor_status(self.BP.PORT_A)
            elif motor == GoniometerObject.ROLL:
                status = self.BP.get_motor_status(self.BP.PORT_B)
            return status
        except IOError as error:
            print(error)

    @staticmethod
    def copy_csv(protocol_file_name, destination_path):
        shutil.copy(protocol_file_name, destination_path + protocol_file_name)

    @staticmethod
    def angle_2_motorpos(angle, motor):
        """Get the motorposition corresponding to an angle for a specific motor"""
        if motor == GoniometerObject.SCATTER:
            return round(8652*7*(angle/360))
        elif motor == GoniometerObject.YAW:
            return round(2700*(angle/360))
        elif motor == GoniometerObject.ROLL:
            return angle*2

        raise ValueError("Motor is not defined in goniometer object")


    def calibrate_led(BP):
        BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)

        value=0;
        BP.set_motor_limits(BP.PORT_C, 100, 1440)
        while value < 1:
            try:

                value = BP.get_sensor(BP.PORT_1)
                BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
                BP.set_motor_position(BP.PORT_C, -1440/6)
            except brickpi3.SensorError as error:
                print(error)

            sleep(1/6)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.
        Zpos=round(8652*7*(270/360))
        BP.set_motor_position(BP.PORT_C, Zpos)

        sleep(Zpos/1440+2)

        BP.reset_all()



    def polarizer(BP,angle):
        BP.set_motor_limits(BP.PORT_D, 100, 1440)
        BP.set_motor_position(BP.PORT_D, angle*3.75)

    @staticmethod
    def read_csv(file_name):
        csvfile1= open(file_name,'r', newline='')
        reader1 = reader(csvfile1,dialect='excel')
        rows=[]
        for row in reader1:
            rows.append(row)
        return rows

    def make_folder(sample_name):
        dir_name=sample_name+"_"+strftime("%Y%m%d_%H%M%S")
        os.makedirs(dir_name)
        return os.getcwd()+os.sep+dir_name+os.sep

    def save_csv(folder,matrix):
        csvfile2=open(folder+'protocole.csv','w', newline='')
        writer2=writer(csvfile2)
        for row in matrix:
            writer2.writerow(row)
        csvfile2.close()

    def my_delay(seconds):
        animation = "|/-\\"
        idx = 0
        while idx<seconds*10:
            print(animation[idx % len(animation)], end="\r")
            idx += 1
            sleep(0.1)

    def welcome():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
                               ______ _____ _____ _   _
                         /\   |  ____/ ____|_   _| \ | |
                        /  \  | |__ | (___   | | |  \| |
                       / /\ \ |  __| \___ \  | | | . ` |
                      / ____ \| |    ____) |_| |_| |\  |
                     /_/    \_\_|   |_____/|_____|_| \_|
       _____             _                      _              ____       _
      / ____|           (_)                    | |            |  _ \     | |
     | |  __  ___  _ __  _  ___  _ __ ___   ___| |_ ___ _ __  | |_) | ___| |_ __ _
     | | |_ |/ _ \| '_ \| |/ _ \| '_ ` _ \ / _ \ __/ _ \ '__| |  _ < / _ \ __/ _` |
     | |__| | (_) | | | | | (_) | | | | | |  __/ ||  __/ |    | |_) |  __/ || (_| |
      \_____|\___/|_| |_|_|\___/|_| |_| |_|\___|\__\___|_|    |____/ \___|\__\__,_|

    """)




