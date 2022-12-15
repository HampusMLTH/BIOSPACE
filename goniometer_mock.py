#!/usr/bin/env python3
from time import sleep, strftime
import os
#from picamera import PiCamera
from csv import reader,writer
#import brickpi3
import shutil
import time

class GoniometerObject(object):
    """ class for Mocking the goniometer"""
    SCATTER = "SCATTER"
    YAW = "YAW"
    ROLL = "ROLL"
    POLARIZER = "POLARIZER"
    
    def __init__(self):
        self.pos_led = 0
        self.pos_stage = 0
        self.pos_sample = 0
        self.pos_polarizer = 
        #self.BP = brickpi3.BrickPi3()
        #self.init_motors()
        
    @property
    def scatter_angle(self):
        """get led angle"""
        pos = self.pos_led
        print("getter")
        angle = pos*360/(7*8652)
        return angle
        
    
    @scatter_angle.setter
    def scatter_angle(self, angle):
        """Set the led angle"""
        print("setter")
        pos1=round(8652*7*(angle/360))
        self.pos_led = pos1
        #sleep(abs(round(8652*7*(angle/360)/1440)+1))
        
    @property
     def yaw_angle(self):
        """get stage angle"""
        pos = self.pos_stage
        angle = pos*360/2700
        return angle
    
    @yaw_angle.setter
    def yaw_angle(self, angle):
        """Set the stage angle"""
        self.pos_stage= angle*2700/360 
        #sleep(angle*2/1440+1)
        
        # move the motor
        #print("moving")
        #print(self.angle_2_motorpos(angle, self.STAGE))
        
    @property
    def roll_angle(self):
        """get sample angle"""
        pos = self.pos_sample
        angle = pos/2
        return angle
    
    @roll_angle.setter
    def roll_angle(self, angle):
        """Set the sample angle"""
       
        pos1=angle*2
        self.pos_sample = pos1
        #sleep(round(2700*(angle/360))/1440+1)
    
    @property
    def polarizer_angle(self):
        pos = self.pos_polarizer
        angle = pos/4.6
        return angle


    @polarizer_angle.setter
    def polarizer_angle(self, angle):
        self.pos_polarizer = angle*4.6

    def init_motors(self):    
        pass
    
    def done_moving(self, motor):
        print("start")
        sleep(1)
        #import random
        #for a in range(1000000):
           
        #    b = random.randint(1,100001)
           
        print("done")
            
    
    def motor_status(self, motor):
        try:
            pass
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
        elif motor == GoniometerObject.POLARIZER:
            return angle*4.6
        
        raise ValueError("Motor is not defined in goniometer object")
    

    def calibrate_led(BP):
        pass


        
    def polarizer(BP,angle):
        pass
        
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





