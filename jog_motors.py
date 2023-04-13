# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/   

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
#import tkinter.messagebox

#from goniometer_mock import GoniometerObject
from goniometer_obj import GoniometerObject

    
class JogMotors(tk.Tk):

    def __init__(self, *args, **kwargs):
  
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "BIOSPACE JOG")

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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.go = GoniometerObject()
        
        button_set_scatter = ttk.Button(self, text="set scatter", command=lambda: self.set_scatter())
        button_set_scatter.grid(row=0, column=0)
        self.scatter_entry = tk.Entry(self)
        self.scatter_entry.grid(row=0,column=1)
        self.scatter_entry.insert(int(self.go.scatter_angle), str(int(self.go.scatter_angle)))

        button_set_yaw = ttk.Button(self, text="set yaw", command=lambda: self.set_yaw())
        button_set_yaw.grid(row=1, column=0)
        self.yaw_entry = tk.Entry(self)
        self.yaw_entry.grid(row=1,column=1)
        self.yaw_entry.insert(int(self.go.yaw_angle), str(int(self.go.yaw_angle)))

        button_set_roll = ttk.Button(self, text="set roll", command=lambda: self.set_roll())
        button_set_roll.grid(row=2, column=0)
        self.roll_entry = tk.Entry(self)
        self.roll_entry.grid(row=2,column=1)
        self.roll_entry.insert(int(self.go.roll_angle), str(int(self.go.roll_angle)))

        button_set_polarizer = ttk.Button(self, text="set polarizer", command=lambda: self.set_polarizer())
        button_set_polarizer.grid(row=3, column=0)
        self.polarizer_entry = tk.Entry(self)
        self.polarizer_entry.grid(row=3,column=1)
        self.polarizer_entry.insert(int(self.go.polarizer_angle), str(int(self.go.polarizer_angle)))
        
        button_exit = ttk.Button(self, text="Exit", command=lambda: self.exit())
        button_exit.grid(row=4, column=0)
                
    
    def exit(self):
        self.go.BP.reset_all()
        quit()
        
    def set_polarizer(self):
        try:
            value = int(self.polarizer_entry.get())
        except ValueError:
            tk.messagebox.showwarning(title="Error", message="Type a number")
        else:
            print("polarizer angle is updated from {} to {}".format(self.go.polarizer_angle,value))
            self.go.polarizer_angle= value

    def set_scatter(self):
        try:
            value = int(self.scatter_entry.get())
        except ValueError:
            tk.messagebox.showwarning(title="Error", message="Type a number")
        else:
            print("scatter angle is updated from {} to {}".format(self.go.scatter_angle,value))
            self.go.scatter_angle= value

    def set_yaw(self):
        try:
            value = int(self.yaw_entry.get())
        except ValueError:
            tk.messagebox.showwarning(title="Error", message="Type a number")
        else:
            print("yaw angle is updated from {} to {}".format(self.go.yaw_angle,value))
            self.go.yaw_angle= value
            

    def set_roll(self):
        try:
            value = int(self.roll_entry.get())
        except ValueError:
            tk.messagebox.showwarning(title="Error", message="Type a number")
        else:
            print("roll angle is updated from {} to {}".format(self.go.roll_angle,value))
            self.go.roll_angle= value
        
    
app = JogMotors()
app.mainloop()
        