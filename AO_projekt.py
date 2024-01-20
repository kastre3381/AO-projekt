from Detection import *

import os
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
from threading import *

class GUI:
	def __init__(self, context):
		self.root = context
		self.root.title("Licence Plate Recognition")
		self.root.resizable(False, False)
		self.root.geometry("800x600")

	def CreateMainFrame(self) :
		self.mainframe = ttk.Frame(self.root)
		self.mainframe.grid()
	
	def CreateImageFrame(self):
		self.imgframe = ttk.Frame(self.mainframe, borderwidth=1, relief="groove", width=800, height=480)
		self.imgframe.grid(column=0, row=0)
		self.imgframe.grid_rowconfigure(0, weight=1)
		self.imgframe.grid_columnconfigure(0, weight=1)
		self.imgframe.grid_propagate(False)
		self.loaded_image = ttk.Label(self.imgframe)

	def CreateMenuFrame(self):
		self.menuframe = ttk.Frame(self.mainframe, borderwidth=1, relief="groove", width=800, height=100, padding="3 3 3 3")
		self.menuframe.grid(column=0, row=2)
		self.menuframe.grid_columnconfigure(1, weight=1)
		self.menuframe.grid_propagate(False)

		Button(self.menuframe, text="Load image", pady=35, command=self.browseFiles).grid(column=0, row=0, rowspan = 2)
		ttk.Label(self.menuframe, text='Recognised plate number:').grid(column=1, row=0)
		self.recognised_number = ttk.Label(self.menuframe)

	def CreateProgressBar(self) :
		self.spacing = ttk.Frame(self.mainframe, width=800, height=20)
		self.spacing.grid(column=0, row=1)
		self.progressBar = ttk.Progressbar(self.spacing, orient='horizontal', length=800, mode='determinate')
		self.progressBar.grid(column=0, row=0)

	def LoadAndRescaleImage(self, filepath : str) :
		currentImage = Image.open(filepath)
		h_scale = 480 / currentImage.height
		w_scale = 800 / currentImage.width
		scale = h_scale if h_scale < w_scale else w_scale
		return currentImage.resize((int(currentImage.width * scale), int(currentImage.height * scale)))

	def LoadImage(self, filepath : str):
		self.image = ImageTk.PhotoImage(self.LoadAndRescaleImage(filepath), master=self.root)
		self.loaded_image.configure(image=self.image)
		self.loaded_image.grid(column=0, row=0)
		self.loaded_image.grid_columnconfigure(0, weight=1)
	
	def PlateToText(self, filename : str):
		self.recognisedNumberText = PlateDetection(filename, Method1, self.progressBar)
		if len(self.recognisedNumberText) == 0 :
			self.recognisedNumberText = PlateDetection(filename, Method2, self.progressBar)
		if len(self.recognisedNumberText) == 0 :
			self.recognisedNumberText = PlateDetection(filename, Method3, self.progressBar)
		if len(self.recognisedNumberText) == 0 :
			self.recognisedNumberText = "not found"
		self.progressBar['value'] = 100


	def LoadPlateNumber(self, filename : str) :
		self.PlateToText(filename)
		self.recognised_number.configure(text = self.recognisedNumberText)
		self.recognised_number.grid(column=1, row=1)

	def browseFiles(self):
		filename = filedialog.askopenfilename(initialdir = os.getcwd(),
										title = "Select an Image",
										filetypes = [("Images", "*.png")])
		self.progressBar['value'] = 0
		self.t1 = Thread(target=lambda : self.LoadPlateNumber(filename))
		self.t1.start()
		self.recognisedNumberText = ""
		self.LoadImage(filename)

root = Tk()
context = GUI(root)
context.CreateMainFrame()
context.CreateProgressBar()
context.CreateImageFrame()
context.CreateMenuFrame()
root.mainloop()
