import os

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import math
from cmath import *
import numpy
import random
import threading

import mandelbrot
import mandelbrot_framework

import newton
import newton_framework

StandartFractalsMethods = ["Mandelbrot", "Newton-Raphson"]
'''StandartFractalsData = {
	"Mandelbrot" : {
		"Type" : "Algebraic",
		"X" : -0.75,
		"Y" : 0.0,
		"Zoom" : 2.25,
		"Formula" : "Z**2 + C",
	},
	"Cubic Mandelbrot" : {
		"Type" : "Algebraic",
		"X" : 0.0,
		"Y" : 0.0,
		"Zoom" : 2.25,
		"Formula" : "Z**3 + C",
	},
	"Quad Mandelbrot" : {
		"Type" : "Algebraic",
		"X" : 0.0,
		"Y" : 0.0,
		"Zoom" : 2.25,
		"Formula" : "Z**4 + C",
	},
	"Burning Ship" : {
		"Type" : "Algebraic",
		"Formula" : "complex(abs(Z.real),abs(Z.imag))**2 + C",
	},
}'''

class App(Tk):
	'''
	def SetupFractalMenu(self, _frac_name):
		global StandartFractalsData
		
		if self.Canvas: self.Canvas.destroy()
		if self.ParametrMenu: self.ParametrMenu.destroy()

		self.CurrentFractalName = _frac_name
		self.CurrentFractalDefualtData = StandartFractalsData[_frac_name]

		if self.CurrentFractalDefualtData["Type"] == "Algebraic":
			self.Canvas = algebraic_framework.FractalCanvas(self)
			self.ParametrMenu = algebraic_framework.ParametrMenu(self, self.Canvas, self.FractalStruct)

			self.ParametrMenu.CoordX.set(0.0 if self.CurrentFractalDefualtData.get("X")==None else self.CurrentFractalDefualtData["X"])
			self.ParametrMenu.CoordY.set(0.0 if self.CurrentFractalDefualtData.get("Y")==None else self.CurrentFractalDefualtData["Y"])
			self.ParametrMenu.CoordZoom.set(1.5 if self.CurrentFractalDefualtData.get("Zoom")==None else self.CurrentFractalDefualtData["Zoom"])
			self.ParametrMenu.Formula.set(self.CurrentFractalDefualtData["Formula"])

	'''

	def save_fractal_iamge(self,event=None):
		if self.Canvas:
			if self.Canvas.Image:
				path = filedialog.asksaveasfilename(title="Выбор файла", initialdir=f"C:\\Users\\{os.getlogin()}\\Pictures", defaultextension="png", initialfile="fractal.png")
				self.Canvas.Image.save(path)

				messagebox.showinfo("Image saved!", f"Image saved!\nPath: {path}")

	def SetupWorkspace(self, _frac_method):
		if self.Canvas: self.Canvas.destroy()
		if self.ParametrMenu: self.ParametrMenu.destroy()

		self.CurrentFractalMethod = _frac_method

		if _frac_method == "Mandelbrot":
			self.Canvas = mandelbrot_framework.FractalCanvas(self)
			self.ParametrMenu = mandelbrot_framework.ParametrMenu(self, self.Canvas, self.FractalStruct)

		elif _frac_method == "Newton-Raphson":
			
			#fract = newton.NewtonRaphson(
			#	50,50,
			#	"Z**3-1",
			#	"3*Z**2",
			#	w=64,
			#	h=64,
			#	m=0.9,
			#	x=0.3,
			#	)
			#fract.getPixels()

			self.Canvas = newton_framework.FractalCanvas(self)
			self.ParametrMenu = newton_framework.ParametrMenu(self, self.Canvas, self.FractalStruct)


	def create_main_menu(self):
		global StandartFractalsMethods

		self.option_add("*tearOff", FALSE)

		fractal_menu_new = Menu()

		for _frac_type in StandartFractalsMethods:
			fractal_menu_new.add_cascade(label=_frac_type,
					command = lambda _frac_type = _frac_type : self.SetupWorkspace(_frac_method=_frac_type))


		'''for frac_type in StandartFractals:
			fractal_group_menu = Menu()
			fractal_menu_new.add_cascade(label=frac_type, menu=fractal_group_menu)
			for frac_name in StandartFractals[frac_type]:
				fractal_group_menu.add_cascade(label=frac_name,
					command = lambda frac_name = frac_name : self.SetupFractalMenu(_frac_name=frac_name))
		'''

		fractal_menu = Menu()
		fractal_menu.add_cascade(label="New", menu=fractal_menu_new)

		#fractal_menu.add_command(label="Save As Project...", command=lambda: print("proj"), accelerator="Ctrl+S")
		#self.bind('<Control-s>', lambda event: print("Saving proj"))		

		fractal_menu.add_command(label="Save As Image...", command=self.save_fractal_iamge, accelerator="Ctrl+Shift+S")
		self.bind('<Control-S>', self.save_fractal_iamge)

		#fractal_menu.add_command(label="Render", command=lambda: print("Render"), accelerator="Ctrl+R")
		#self.bind('<Control-r>', lambda event: print("Rendering"))

		fractal_menu.add_separator()

		fractal_menu.add_command(label="Load preset...", accelerator="Ctrl+P")

		fractal_menu.add_separator()
		fractal_menu.add_cascade(label="Exit")

		main_menu = Menu()
		main_menu.add_cascade(label="Fractal", menu=fractal_menu)
		#main_menu.add_cascade(label="Edit")
		main_menu.add_cascade(label="Help")
		self.config(menu=main_menu)

	def __init__(self):

		self.CurrentFractalMethod = None
		self.CurrentFractalDefualtData = None

		self.FractalStruct = None
		self.ParametrMenu = None
		self.Canvas = None

		super().__init__()

		self.title("Fractalio")
		self.geometry("800x500")

		self.create_main_menu()

		self.SetupWorkspace("Newton-Raphson")

if __name__ == '__main__':
	app = App()
	app.mainloop()
