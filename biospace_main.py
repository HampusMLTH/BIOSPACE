# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/   


# TODO: browse folder to initiate bc
#move variables to bc such as dynamic range
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
#import tkinter.messagebox

import os
import time
import timeit
from basler_controller import BaslerController
#from basler_controller_mock import BaslerController
import sys
import numpy as np
import matplotlib.pyplot as plt
import shutil

from queue import Queue
from queue import Empty
import threading

#from goniometer_mock import GoniometerObject
from goniometer_obj import GoniometerObject

MAX_QSIZE = 99
LED_WAVELENGTHS = ["background",
                   "365 nm",
                   "405 nm",
                   "430 nm",
                   "490 nm",
                   "525 nm",
                   "630 nm",
                   "810 nm",
                   "940 nm",]
PLOT_COLORS = [(.85,.85,.54),
               (.7,.7,.7),
               (.7,0,.7),
               (.5,0,.9,),
               (.4,0.9,.8),
               (.0,1,.0),
               (1,0,.0),
               (.5,0.5,.5),
               (.1,.1,.1),]
LED_SAVENAMES = ["background",
                 "365nm",
                 "405nm",
                 "430nm",
                 "940nm",
                 "490nm",
                 "525nm",
                 "630nm",
                 "810nm",]
#FIELDS = ["ExposureTimeRaw",
#         "GainRaw",
#          "AqcuisitionRateRaw"]
FIELDS = ["ExposureTime",
          "Gain\t",
          "AcquisitionFrameRate"]
UNITS = ["µs",
          "linear gain",
          "?"]
LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(10,7), dpi=100)
fig_image = f.add_subplot(211)
fig_hist = f.add_subplot(212)
#folder_path = "/home/pi/Desktop/BrickPi3-master/Software/Python/Testing Scripts/pypylon/images/" 
#folder_path = "/" + time.strftime("%Y%m%d-%H%M%S/")
#test_folder = filedialog.askdirectory(initialdir = "/", title = "Choose destination folder")
#test_folder = "C:/Users/Hampus/Desktop/testtest"
#folder_path = test_folder + time.strftime("/%Y%m%d-%H%M%S/")

#bc = BaslerController(folder_path, q)






    

def animate(i):
    pass #not used?
    
            

class GoniometerApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        
        self.nbr_exposures = 9
        self.led_background_list = []
        tk.Tk.__init__(self, *args, **kwargs)
        test_folder = "/home/pi/meas"#filedialog.askdirectory(initialdir = "/", title = "Choose destination folder")
        folder_path = test_folder + time.strftime("/%Y-%m-%d_%H%M_%S/")
        self.q = Queue(maxsize=MAX_QSIZE)
        self.bc = BaslerController(folder_path, self.q)
        self.o_exp_px=np.empty((0,8),int)
        #self.go = GoniometerMock()
        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "BIOSPACE")
        
        
    
        
        self.container = tk.Frame(self)
        #self.container.pack(side="top", fill="both", expand = True)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        
        
        for F in (StartPage, ):

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(bg="gray")
            frame.grid_rowconfigure(10, weight=1)
            
            

        
        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):
    class_canvas = None
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        #label = tk.Label(self, text="Gonio", font=LARGE_FONT)
        #label.pack(pady=10,padx=10)
        self.controller = controller
        StartPage.class_canvas = FigureCanvasTkAgg(f, self)
        self._calibrating = False
        self._calibrating_iteration = 0
        self._calibrated_background = None 
        self.protocol_filename = "/home/pi/Dexter/BrickPi3/Software/Python/biospace/protocol.csv"
        #"E:\measurements\protocol_test.csv"
        #r"C:\Users\Hampus\Desktop\testtest\protocol_test.csv" 
        #"E:\measurements\protocol_test.csv"
        self.protocol_nbr_rows = None
        #self.protocol_index = None
        
        

        button_start_cam = ttk.Button(self, text="start camera",
                            command=lambda: self.update_graph())
        button_start_cam.grid(row=0, column=0)
        
        button_stop_cam = ttk.Button(self, text="stop camera",
                            command=lambda: self.close_camera())
        button_stop_cam.grid(row=0, column=1)
        
        button_read_value = ttk.Button(self, text="read value",
                            command=lambda: self.get_nodemap_value())
        button_read_value.grid(row=1,column=0)
        
        button_set_value = ttk.Button(self, text="set value",
                            command=lambda: self.update_nodemap_field())#e.get()))
        button_set_value.grid(row=1,column=1)


        self.field_combo = ttk.Combobox(self, values=FIELDS, state="readonly")
        self.field_combo.grid(row=2, column=0)
        self.field_combo.current(0)
        self.value_entry = tk.Entry(self)
        self.value_entry.grid(row=2,column=1)
        self.value_entry.insert(0, "value...")
        
        self.unit_label = tk.Label(self, text="")
        self.unit_label.grid(row=2,column=2)
        
        
    
        button_choose_protocol = ttk.Button(self, text="choose protocol file",
                            command=lambda: self.file_dialog())
        button_choose_protocol.grid(row=3,column=0,columnspan=3)
        self.label_protocol_filename = ttk.Label(self, text=self.protocol_filename)
        self.label_protocol_filename.grid(row=4,column=0,columnspan=3)
        
        button_nodefile = ttk.Button(self, text="choose camera param file",
                                        command=lambda: self.nodefile_dialog())
        button_nodefile.grid(row=5,column=0,columnspan=3)
        self.label_nodefile = ttk.Label(self, text=self.controller.bc.nodefile)
        self.label_nodefile.grid(row=6,column=0,columnspan=3)

        button_save_folder = ttk.Button(self, text="choose save directory",
                                        command=lambda: self.folder_dialog())
        button_save_folder.grid(row=7,column=0,columnspan=3)
        self.label_save_folder = ttk.Label(self, text=self.controller.bc.folder_path)
        self.label_save_folder.grid(row=8,column=0,columnspan=3)
        
        
        red_label = tk.Label(self, text="preview image: red band")
        red_label.grid(row=11, column=0)
        self.red_LED = ttk.Combobox(self, values=LED_WAVELENGTHS, state="readonly")
        self.red_LED.grid(row=11,column=1, columnspan=2)
        self.red_LED.current(5)

        green_label = tk.Label(self, text="preview image: green band")
        green_label.grid(row=12, column=0)
        self.green_LED = ttk.Combobox(self, values=LED_WAVELENGTHS, state="readonly")
        self.green_LED.grid(row=12,column=1, columnspan=2)
        self.green_LED.current(4)

        blue_label = tk.Label(self, text="preview image: blue band")
        blue_label.grid(row=13, column=0)
        self.blue_LED = ttk.Combobox(self, values=LED_WAVELENGTHS, state="readonly")
        self.blue_LED.grid(row=13,column=1, columnspan=2)
        self.blue_LED.current(2)


        button_set_preview_gain = ttk.Button(self, text="set preview gain", command=lambda: self.set_preview_gain())#e.get()))
        button_set_preview_gain.grid(row=14,column=0)
        self.preview_gain_entry = tk.Entry(self)
        self.preview_gain_entry.grid(row=14,column=1)
        self.preview_gain_entry.insert(0, "1")
        self.preview_gain=1;



        self.display_cb = tk.IntVar()
        ttk.Checkbutton(self, text="display live image", variable=self.display_cb).grid(row=15, column=0, sticky=tk.E)
        self.display_cb.set(1)
        
        self.display_hist_cb = tk.IntVar()
        ttk.Checkbutton(self, text="display histogram", variable=self.display_hist_cb).grid(row=15, column=1, sticky=tk.E)
        self.display_hist_cb.set(1)
        
        self.save_cb = tk.IntVar()
        ttk.Checkbutton(self, text="save images", variable=self.save_cb).grid(row=15, column=2, sticky=tk.E)
        
        
        button_start_led_calibration = ttk.Button(self, text="start LED calibration",
                            command=lambda: self.start_led_calibration())
        button_start_led_calibration.grid(row=16,column=0,columnspan=2)
        self.led_calibration_label = tk.Label(self, text="no calibration")
        self.led_calibration_label.grid(row=16, column=3)

        button_start_measurement = ttk.Button(self, text="start measurement",
                            command=lambda: self.start_measurement())
        button_start_measurement.grid(row=17,column=0,columnspan=2)
        self.measuring_label = tk.Label(self, text="")
        self.measuring_label.grid(row=17, column=3)
        # TODO: when measurement is started make sure to copy nodefile to dest..

        StartPage.class_canvas.draw()
        StartPage.class_canvas.get_tk_widget().grid(row=0, rowspan=18, column=3, sticky = "se")

        #toolbar = NavigationToolbar2Tk(StartPage.class_canvas, self)
        #toolbar.update()
        StartPage.class_canvas._tkcanvas.grid(row=0, rowspan=18, column=3, sticky = "se", pady=0)
        
        #controller.container.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(3, weight=2)
        # column 3 should expand to allow image to be as large as possible
        #same logic with row 10
        
        self.ani = animation.FuncAnimation(f, StartPage.draw, interval=2000)
        
    def start_led_calibration(self):
        print("LED calibration started\n make sure room lighting is low and static, make sure your sample is well lit by the LEDs")
        print("If your sample is small or dark, use a white paper for the calibration")
        self.led_calibration_label["text"] = "Calibrating"
        # do 10 loops
        self._calibrating = True;

    def start_measurement(self):
        print("test start meas")
        if self.protocol_filename is None:
            self.protocol_filename = self.file_dialog()
        
        self.measuring_label["text"] = "MEASURING"
        
        #self.go.copy_csv(self.protocol_filename, self.controller.bc.folder_path)
        #self.wait_thread = threading.Thread(target=self.wait_thread)
        
            
            #self.wait_thread()
            #self.wait_thread.start()
            #self.wait_thread.join()
            #print("-----------SAVE IMAGES")
    def wait_4_motors(self):
        #print("in wait thread")
        self.go.done_moving(self.go.SCATTER)
        self.go.done_moving(self.go.YAW)
        self.go.done_moving(self.go.ROLL)
        #print("end of wait thread")
        
    def file_dialog(self):
        self.protocol_filename = filedialog.askopenfilename(title = "Choose protocol", filetypes = (("CSV Files","*.csv"),))
        self.label_protocol_filename.configure(text=self.protocol_filename)
    
    def nodefile_dialog(self):
        self.controller.bc.nodefile = filedialog.askopenfilename(initialdir = "/", title = "Choose nodefile for camera parameters")
        self.label_nodefile.configure(text=self.controller.bc.nodefile)
        
    def folder_dialog(self):
        folder_parent = filedialog.askdirectory(initialdir = "/", title = "Choose destination folder")
        self.controller.bc.folder_path = folder_parent + time.strftime("/%Y-%m-%d_%H%M_%S/")
        self.label_save_folder.configure(text=self.controller.bc.folder_path)
        os.mkdir(self.controller.bc.folder_path)
    
    def draw(i):
        StartPage.class_canvas.draw()
        #print("redrawing")
            
    
    def close_camera(self):
        self.stop_live_view()
        self.controller.bc.stop_cont_acq()
        self.controller.bc.close_camera()
    
    def move_1(self, d):
        if len(d)==3:
            print("moving to scatter: {}, yaw: {},roll: {} ".format(d[0],d[1],d[2]))
            self.go.scatter_angle = int(d[0])
            self.go.yaw_angle = int(d[1])
            self.go.roll_angle = int(d[2])
        elif len(d)==4:
            print("moving to scatter: {}, yaw: {},roll: {}, polarizer {} ".format(d[0],d[1],d[2],d[3]))
            self.go.scatter_angle = int(d[0])
            self.go.yaw_angle = int(d[1])
            self.go.roll_angle = int(d[2])
            self.go.polarizer_angle = int(d[3])
        
        self.wait_4_motors()
        
    def consumer_thread(self, stop):
        #
        print("in thread")
        temp = 0
        while not stop():
            start_time = time.time()
            temp += 1
            #print("stop is {}".format(stop()))
            i = 0
            images = []
            if self.measuring_label["text"]:
                if self.protocol_nbr_rows is None:
                    print("START MEASURING")
                    self.controller.bc.copy_nodemap()
                    self.protocol = GoniometerObject.read_csv(self.protocol_filename)
                    self.go = GoniometerObject()
                    #self.protocol = GoniometerMock.read_csv(self.protocol_filename)
                    #self.go = GoniometerMock()
                    
                    self.protocol_nbr_rows = len(self.protocol)
                    self.protocol_index = -1
                if self.protocol_index == self.protocol_nbr_rows-1: # done with protocol
                    self.measuring_label["text"] = ""
                    self.save_cb.set(0)
                    np.savetxt(self.controller.bc.folder_path + 'over_exposed.csv', self.controller.o_exp_px, delimiter=',',fmt='%d')
                    shutil.copy(self.protocol_filename, self.controller.bc.folder_path + 'protocol.csv')
                else:
                    self.protocol_index = self.protocol_index + 1
                    self.move_1(self.protocol[self.protocol_index])
                    #for d in protocol:
                    while (self.controller.q.qsize())%9 != 0:
                        #time.sleep(0.001)
                        pass
                    #with self.controller.q.mutex:
                    #print((self.controller.q.qsize()))
                    #print("CLEARING QUEUE")
                    self.controller.q.queue.clear()
                    #TODO: this is a little dangerous if an element is added before clearing.. 
                    # instead clear 9*x times untill all are removed..
                    
                    self.save_cb.set(1)
               
            while i < 9:

                #img = plt.imread("sample_imgs/{}.tiff".format(i))

                try:
                    img = self.controller.q.get(timeout=3)
                except Empty:
                    print("timeout reached, i is {}".format(i))
                    if stop():
                        break
                else:
                    # (if no error)
                    images.append(img.astype('int16'))
                    self.controller.q.task_done()
                    
                    i += 1
             
            
           
            
            #self.canvas.draw()
            #print("show images now")
            #print("display checkbox is --------------- {}".format(self.display_cb.get()))
            #print("save checkbox is --------------- {}".format(self.save_cb.get()))
            self.show_color_image(images, temp)
            end_time = time.time()
            new_interval = int((end_time - start_time)*1000)
            #print("updating interval to {}".format(new_interval))
            self.ani.event_source.interval = new_interval
        
            
        #print("bottom")
            

    def show_color_image(self, images, temp):
        #add option of chosing red green blue leds
        #print("show colorim")
        #print("red is {} green is {} blue is {}".format(self.red_LED.get(), 
        #                                                self.green_LED.get(), 
        #                                                self.blue_LED.get(),))
        #self.comboExample.current()
        
        dynamic_range = 4095#65520
        darkest_img_mean = sys.maxsize
        index_background = None

        i = 0
        fig_hist.clear()
        mean_values=[0]*8
        max_values=[0]*8
        nbr_overexp_px=[0]*8
        for image in images:
            img_mean = np.around(image.mean(), 2)
            img_max = np.around(image.max(), 2)
            if self.display_hist_cb.get():
                
                if self._calibrated_background is None:
                    plot_index = i % 9
                    fig_hist.hist(image.flatten(), 32, label='LED {}'.format(i), alpha=0.8, histtype="step")
                else:
                    plot_index = (i - self._calibrated_background) % 9
                    fig_hist.hist(image.flatten(), 32, label=LED_SAVENAMES[plot_index], alpha=0.8, histtype="step", color=PLOT_COLORS[plot_index])
                fig_hist.plot(img_mean, 10000, 'o', color=PLOT_COLORS[plot_index])
            print("LED {} has a mean of: {} plot_index:{}, color:{}, MAX={}".format(i, img_mean, plot_index, LED_SAVENAMES[plot_index], img_max))
            mean_values[plot_index-1]=img_mean
            max_values[plot_index-1]=img_max
            if img_max == dynamic_range:
                nbr_overexp_px[plot_index-1]=np.count_nonzero(image==dynamic_range)
            if img_mean < darkest_img_mean:
                darkest_img_mean = img_mean
                index_background = i
            i += 1
    
        print(LED_WAVELENGTHS[1:])
        print('mean: ', *mean_values, sep=', ')
        print('max: ', *max_values, sep=', ')
        print("off is LED {} with mean: {} comp to {}".format(index_background, darkest_img_mean, np.mean(mean_values)))
        print('Number of overexposed pixels: {}'.format(nbr_overexp_px))
        
        

        if self.display_hist_cb.get():
            fig_hist.legend(bbox_to_anchor=(0,-0.2,1,0.2), loc="upper left",
                mode="expand", borderaxespad=0, ncol=5)
        if self._calibrating:
            self.controller.led_background_list.append(index_background)
            self._calibrating_iteration = self._calibrating_iteration + 1
            led_iterations=10;
            if self._calibrating_iteration >= led_iterations:
                self._calibrating = False
                self._calibrated_background = max(set(self.controller.led_background_list),key=self.controller.led_background_list.count)
                calibration_success = 100*self.controller.led_background_list.count(self._calibrated_background)/led_iterations
                print("led number which was dark")
                print(*self.controller.led_background_list)
                print("--------------------")
                if calibration_success >= 80:
                    self.led_calibration_label["text"] = "Calibration done, LED {}, {}%".format(
                    self._calibrated_background, calibration_success)
                else:
                    self.led_calibration_label["text"] = "Calibration failed, LED {}, {}%".format(
                    self._calibrated_background, calibration_success)
                self._calibrating_iteration = 0
                self.controller.led_background_list = []
        # if not self.measuring_label["text"]:
        #     self.controller.led_background_list.append(index_background)
        # else: # dont change while doing measurements.. todo: make separe button to stop changing off
        #     old_background = int(np.rint(np.median(self.controller.led_background_list)))
        #     index_background = old_background
        # old_background = int(np.rint(np.median(self.controller.led_background_list)))

        if self._calibrated_background is None:
            print("OBS not calibrated")
            print(self._calibrated_background)
        elif index_background != self._calibrated_background:
            print("------------------------------WARNING-------------------------------")
            print("measured background LED {} is deviating from previous background {}".format(index_background, self._calibrated_background))
            print("--------------------------------------------------------------------")
            index_background=self._calibrated_background



        #     print("------------------------------WARNING-------------------------------")
        #     print("measured background LED {} is deviating from previous background {}".format(
        #         index_background, old_background))
        #     print("--------------------------------------------------------------------")
        #     index_background = old_background
        
        
        #calibration_coef=[1, 1, 6, 1.8, 1.1, 1.3, 60, 2, 5] # coefficients to make a flat field, 365 and 630 switched location so starting [630, 405, 430,.. 
        #todo fix what colors
        img_background =images[index_background]
        processed_img = [img_background] # this list will contain bkg and then bkg subtracted images in increasing wavelengths same order as LED_WAVELENGTHS
        for s in range(0,len(LED_WAVELENGTHS) - 1):
            current_image = (images[(index_background + s + 1) % 9])
            current_image = (current_image.astype(float)/dynamic_range)
            #current_image = (current_image.astype(float)*calibration_coef[(index_background + s + 1) % 9]/dynamic_range).clip(max=1)
            processed_img.append(current_image)
        processed_img[0] =   processed_img[0].astype(float)/dynamic_range # normalize background
        
        if self.display_cb.get():
            self.color_img = np.ndarray(shape=(processed_img[1].shape + (3,)),dtype=float)
            self.color_img[:,:,0] = processed_img[self.red_LED.current()]
            self.color_img[:,:,1] = processed_img[self.green_LED.current()]
            self.color_img[:,:,2] = processed_img[self.blue_LED.current()]
            self.color_img = self.color_img * self.preview_gain
            self.color_img = np.clip(self.color_img, 0, 1)
            fig_image.clear()
            fig_image.imshow(self.color_img)
            fig_image.grid(None)
        
        if self.save_cb.get():
            import imageio
            pos_str=""
            if self.measuring_label["text"]:
                pos = self.protocol[self.protocol_index]
                pos_str = ""
                if len(pos)==3:
                    pos_str = "scatter_{}_yaw_{}_roll_{}/".format(pos[0], pos[1], pos[2])
                else:
                    pos_str = "scatter_{}_yaw_{}_roll_{}_polarization_{}/".format(pos[0], pos[1], pos[2], pos[3])
                if not os.path.isdir(self.controller.bc.folder_path + pos_str):
                    os.mkdir(self.controller.bc.folder_path + pos_str)
                self.controller.o_exp_px = np.append(self.controller.o_exp_px,np.array([nbr_overexp_px]), axis=0)
                #print(self.controller.o_exp_px)
            for n, led in enumerate(LED_SAVENAMES):
                imageio.imwrite(self.controller.bc.folder_path + pos_str + "{}.tiff".format(led), processed_img[n])
            #imageio.imwrite(self.controller.bc.folder_path + pos_str + "{}_color_image.tiff".format(temp), self.color_img)
            
            #TODO: just add all colors
            #TODO need to have a stable way of finding off index
            #TODO: need to fix legend so it says actual wavelengths
            
            #TODO: save to folder directly

       
    
    def update_nodemap_field(self):
        try:
            value = int(self.value_entry.get())
        except ValueError:
            tk.messagebox.showwarning(title="Error", message="Type a number")
        else:
            self.controller.bc.update_nodemap_value(self.field_combo.get(), value)
            self.unit_label["text"] = UNITS[self.field_combo.current()]
            print("{} is updated to {}".format(self.value_entry.get(), value))
    
    def set_preview_gain(self):
        try:
            value = int(self.preview_gain_entry.get())
        except ValueError:
            tk.messagebox.showwarning(title="Error", message="Type a number")
        else:
            self.preview_gain = value
            
            print("preview gain is updated to {}".format(self.preview_gain))        

    
    def get_nodemap_value(self):
        print(self.controller.bc.get_nodemap_value(self.field_combo.get()))
        self.value_entry.delete(0, tk.END)
        self.value_entry.insert(0,str(self.controller.bc.get_nodemap_value(self.field_combo.get())))
        
        self.unit_label["text"] = UNITS[self.field_combo.current()]
    
    def start_live_view(self):
        self.controller.led_background_list = []
        self.stop_threads = False
        self.cons_thread = threading.Thread(target=self.consumer_thread, args =(lambda : self.stop_threads, ))
        self.cons_thread.start()
    
    def stop_live_view(self):
        self.stop_threads = True
        #self.cons_thread.join()
        
    def update_graph(self):
        
        self.controller.bc.open_camera()
        self.controller.bc.update_nodemap()
        
        self.controller.bc.cont_acq()
        stop_threads = False
        #consumer_thread = threading.Thread(target=self.consumer_thread, args =(lambda : stop_threads, ))
        #consumer_thread.start()
        print("thread started")
        self.start_live_view()
        #time.sleep(1)
        #stop_threads = True
        #consumer_thread.join()
        
        


    def help_method(self):
        self.controller.led_background = 0
        print(self.controller.led_background)


app = GoniometerApp()
#ani = animation.FuncAnimation(f, animate, interval=2000)


#app.ani = animation.FuncAnimation(f, StartPage.draw, interval=2000)

app.mainloop()
        
