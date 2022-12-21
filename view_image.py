# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/   

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import imageio

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
#import tkinter.messagebox


LED_WAVELENGTHS = ["background",
                   "365 nm",
                   "405 nm",
                   "430 nm",
                   "490 nm",
                   "525 nm",
                   "630 nm",
                   "810 nm",
                   "940 nm",]
LED_SAVENAMES = ["background",
                 "365_nm",
                 "405_nm",
                 "430_nm",
                 "940_nm",
                 "490_nm",
                 "525_nm",
                 "630_nm",
                 "810_nm",]

f = Figure(figsize=(10,7), dpi=100)

fig_1 = f.add_subplot(211)
fig_2 = f.add_subplot(212)

    
class ViewImage(tk.Tk):

    def __init__(self, *args, **kwargs):
  
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "BIOSPACE VIEW IMAGE")

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
        self.controller = controller
        self.folder = ""
        StartPage.class_canvas = FigureCanvasTkAgg(f, self)
        button_folder = ttk.Button(self, text="Select folder", command=lambda: self.folder_dialog())
        button_folder.grid(row=0, column=0)
        self.label_foldername = ttk.Label(self, text=self.folder, width=20)
        self.label_foldername.grid(row=0,column=1)
        


        fig_1_label = tk.Label(self, text="preview image 1:")
        fig_1_label.grid(row=1, column=0)
        self.fig_1_LED = ttk.Combobox(self, values=LED_WAVELENGTHS, state="readonly")
        self.fig_1_LED.grid(row=1,column=1)
        self.fig_1_LED.current(0)

        fig_2_label = tk.Label(self, text="preview image 2:")
        fig_2_label.grid(row=2, column=0)
        self.fig_2_LED = ttk.Combobox(self, values=LED_WAVELENGTHS, state="readonly")
        self.fig_2_LED.grid(row=2,column=1)
        self.fig_2_LED.current(0)

        button_folder = ttk.Button(self, text="Update", command=lambda: self.show_images())
        button_folder.grid(row=3, column=0)

        StartPage.class_canvas.draw()
        StartPage.class_canvas.get_tk_widget().grid(row=0, rowspan=18, column=3, sticky = "se")

        #toolbar = NavigationToolbar2Tk(StartPage.class_canvas, self)
        #toolbar.update()
        StartPage.class_canvas._tkcanvas.grid(row=0, rowspan=18, column=3, sticky = "se", pady=0)
        self.grid_columnconfigure(3, weight=2)

        
    def folder_dialog(self):
        self.folder = filedialog.askdirectory(initialdir = "/", title = "Choose destination folder")
        self.label_foldername.configure(text=self.folder)

    def show_images(self):
        filename = self.folder + '/{}.tiff'.format(LED_SAVENAMES[self.fig_1_LED.current()])
        print(filename)
        image_1 = imageio.imread(filename)
        fig_1.clear()
        fig_1.imshow(image_1)
        fig_1.grid(False)

        filename = self.folder + '/{}.tiff'.format(LED_SAVENAMES[self.fig_2_LED.current()])
        print(filename)
        image_2 = imageio.imread(filename)
        fig_2.clear()
        fig_2.imshow(image_2)
        fig_2.grid(False)

        StartPage.class_canvas.draw()
        
    
app = ViewImage()
app.mainloop()
        