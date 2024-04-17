from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import math
from cmath import *
import numpy
import random

from PIL import Image, ImageTk, ImageDraw

import threading
import time
import matplotlib
import matplotlib.cm
import matplotlib.pyplot

from error_for_canvas import ErrorMessage
from mandelbrot import Mandelbrot

class ParametrMenu(ttk.Frame):

	def create_julia_menu(self):

		if self.BuildAsJuliaEnable.get() == 0:
			if self.JuliaMenu:
				self.JuliaMenu.destroy()
		else:

			julia_frame = ttk.Frame(self.FormulaFrame, relief="solid")
			julia_frame.pack(anchor=W, fill=X, padx=5, pady=5)

			grid_frame = ttk.Frame(julia_frame)
			grid_frame.pack(anchor=W, fill=X, padx=5, pady=5)
			grid_frame.columnconfigure(index=0, weight=1)
			grid_frame.columnconfigure(index=1, weight=10)
			ttk.Label(grid_frame, text="X: ").grid(column=0, row=0, sticky="e", pady=2)
			ttk.Label(grid_frame, text="Y: ").grid(column=0, row=1, sticky="e", pady=2)
			e_x = ttk.Entry(grid_frame, textvariable=self.JuliaCoordX)
			e_x.grid(column=1,row=0, sticky="ew")
			e_y = ttk.Entry(grid_frame, textvariable=self.JuliaCoordY)
			e_y.grid(column=1,row=1, sticky="ew")

			self.JuliaMenu = julia_frame

	def create_gui(self):

		self.ItemForDisable = []

		self.GlobalTabMenu = ttk.Notebook(self)
		self.GlobalTabMenu.pack(anchor=NW,fill=BOTH,expand=True)
		self.GlobalTabMenu.grid_propagate(False)
		self.GlobalTabMenu.pack_propagate(False)

		################ PROPERTIES MENU ############

		self.Properties = ttk.Frame(self.GlobalTabMenu)
		self.Properties.pack(anchor=NW, fill=BOTH, expand=True)
		self.GlobalTabMenu.add(self.Properties, text="Properties")
		
		### FORMULA
		formula_frame = ttk.Frame(self.Properties, relief="solid")
		formula_frame.pack(anchor=W, fill=X, padx=5, pady=5)
		self.FormulaFrame = formula_frame
		ttk.Label(formula_frame, text="Formula", anchor="n").pack(anchor=W, fill=X, padx=2, pady=2)
		e_f = ttk.Entry(formula_frame, textvariable=self.Formula)
		e_f.pack(anchor=W, fill=X, padx=5)
		self.ItemForDisable.append(e_f)
		self.ApplyButton = ttk.Button(formula_frame, text="Apply")
		self.ApplyButton.pack(anchor=W, fill=X, padx=5, pady=5)
		self.ItemForDisable.append(self.ApplyButton)

		self.BuildAsJuliaEnable = IntVar()
		self.JuliaMenu = None
		ttk.Checkbutton(formula_frame, text="Build as Julias set", variable=self.BuildAsJuliaEnable, command=self.create_julia_menu).pack(anchor=W, fill=X, padx=5, pady=5)

		### COORDINATES
		coor_frame = ttk.Frame(self.Properties, relief="solid")
		coor_frame.pack(anchor=W, fill=X, padx=5, pady=5)
		ttk.Label(coor_frame, text="Coordinates", anchor="n").pack(anchor=W, fill=X, padx=2, pady=2)

		grid_frame = ttk.Frame(coor_frame)
		grid_frame.pack(anchor=W, fill=X, padx=5, pady=5)
		grid_frame.columnconfigure(index=0, weight=1)
		grid_frame.columnconfigure(index=1, weight=10)

		ttk.Label(grid_frame, text="X: ").grid(column=0, row=0, sticky="e", pady=2)
		ttk.Label(grid_frame, text="Y: ").grid(column=0, row=1, sticky="e", pady=2)
		ttk.Label(grid_frame, text="Zoom: ").grid(column=0, row=3, sticky="e", pady=2)

		e_x = ttk.Entry(grid_frame, textvariable=self.CoordX)
		e_x.grid(column=1,row=0, sticky="ew")
		e_y = ttk.Entry(grid_frame, textvariable=self.CoordY)
		e_y.grid(column=1,row=1, sticky="ew")
		e_zoom = ttk.Entry(grid_frame, textvariable=self.CoordZoom)
		e_zoom.grid(column=1,row=3, sticky="ew")
		self.ItemForDisable.extend([e_x,e_y,e_zoom])

		### ADVANCED PROPERTIES
		advan_frame = ttk.Frame(self.Properties, relief="solid")
		advan_frame.pack(anchor=W, fill=X, padx=5, pady=5)
		ttk.Label(advan_frame, text="Advanced properties", anchor="n").pack(anchor=W, fill=X, padx=2, pady=2)

		################ PROPERTIES MENU ############

		############### RENDER MENU ###########

		self.Render = ttk.Frame(self.GlobalTabMenu)
		self.Render.pack(anchor=NW, fill=BOTH, expand=True)
		self.GlobalTabMenu.add(self.Render, text="Render")

		### QUALITY
		quality_frame = ttk.Frame(self.Render, relief="solid")
		quality_frame.pack(anchor=W, fill=X, padx=5, pady=5)
		ttk.Label(quality_frame, text="Render Quality", anchor="n").pack(anchor=W, fill=X, padx=2, pady=2)

		grid_frame = ttk.Frame(quality_frame)
		grid_frame.pack(anchor=W, fill=X, padx=5, pady=5)
		grid_frame.columnconfigure(index=0, weight=1)
		grid_frame.columnconfigure(index=1, weight=10)

		ttk.Label(grid_frame, text="Resolution: ").grid(column=0,row=0,sticky="ew")
		s_res = ttk.Spinbox(grid_frame, from_=64, to=4096, textvariable=self.Resolution)
		s_res.grid(column=1,row=0,sticky="ew")
		self.ItemForDisable.append(s_res)

		ttk.Label(grid_frame, text="Iterations: ").grid(column=0,row=1,sticky="ew")
		s_it = ttk.Spinbox(grid_frame, from_=1, to=4096, textvariable=self.Iterations)
		s_it.grid(column=1,row=1,sticky="ew")
		self.ItemForDisable.append(s_it)

		### PALETTE 

		palette_menu = ttk.Frame(self.Render, relief="solid")
		palette_menu.pack(anchor=W, fill=X, padx=5, pady=5)
		ttk.Label(palette_menu, text="Palette", anchor="n").pack(anchor=W, fill=X, padx=2, pady=2)

		current_palette_name = ttk.Label(palette_menu, text="Palette: " + self.PaletteName.get(), anchor="w")
		current_palette_name.pack(anchor=W, fill=X, padx=5, pady=2)

		scrollbar = ttk.Scrollbar(palette_menu)
		listbox = ttk.Treeview(palette_menu, yscrollcommand=scrollbar.set, show="tree")
		scrollbar.configure(command=listbox.yview)

		scrollbar.pack(side="right", fill="y", padx=5, pady=5)
		listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

		custom_palette = ["hsv", "flag", "twilight"]
		for i in custom_palette:#matplotlib.pyplot.colormaps():
		    listbox.insert("", "end", text=i)

		def item_selected(event):
			n = listbox.item(listbox.selection())["text"]
			current_palette_name.config(text="Palette: " + n)
			self.PaletteName.set(n)
		 
		listbox.bind("<<TreeviewSelect>>", item_selected)

		############### RENDER MENU ###########


		################# ZOOM BUTTONS #############
		frame = Frame(self.Canvas, width=40, height=80)
		frame.pack_propagate(False) 
		frame.pack(anchor=N, side=LEFT)

		self.ZoomInButton = ttk.Button(frame, text="Z+")
		self.ZoomOutButton = ttk.Button(frame, text="Z-")

		self.ZoomInButton.pack(anchor=W, fill=BOTH, expand=True)
		self.ZoomOutButton.pack(anchor=W, fill=BOTH, expand=True)

		self.ItemForDisable.extend([self.ZoomInButton, self.ZoomOutButton])

	def setup_fract_struct(self):
		self.FractalStruct = None
		self.FractalStruct = Mandelbrot(
			self.Canvas.Width,
			self.Canvas.Height,
			self.Formula.get(),
			self.CoordX.get(),
			self.CoordY.get(),
			self.CoordZoom.get(),
			iterations=self.Iterations.get(),
			w=self.Resolution.get(),
			h=self.Resolution.get(),
			buildAsJulia=self.BuildAsJuliaEnable.get(),
			jX = self.JuliaCoordX.get(),
			jY = self.JuliaCoordY.get(),
		)

	def start_draw_after_hotkey(self):
		self.start_draw_after_apply()		

	def start_draw_after_apply(self):
		self.setup_fract_struct()

		self.start_render()

	def start_draw_after_move(self, event):
		self.setup_fract_struct()

		self.FractalStruct.shiftView(event)

		self.CoordX.set(self.FractalStruct.xCenter)
		self.CoordY.set(self.FractalStruct.yCenter)

		self.start_render()

	def start_draw_after_zoomIn(self):
		self.setup_fract_struct()

		self.FractalStruct.zoomInXY(self.FractalStruct.xCenter, self.FractalStruct.yCenter)

		self.CoordX.set(self.FractalStruct.xCenter)
		self.CoordY.set(self.FractalStruct.yCenter)
		self.CoordZoom.set(self.FractalStruct.delta)

		self.start_render()

	def start_draw_after_zoomOut(self):
		self.setup_fract_struct()

		self.FractalStruct.zoomOutXY(self.FractalStruct.xCenter, self.FractalStruct.yCenter)

		self.CoordX.set(self.FractalStruct.xCenter)
		self.CoordY.set(self.FractalStruct.yCenter)
		self.CoordZoom.set(self.FractalStruct.delta)

		self.start_render()

	def start_render(self):
		self.RenderNow = True
		self.RenderThread = threading.Thread(target=self.draw_process)
		self.RenderThread.start()

		self.Canvas.RenderStateLabel.config(foreground="black")
		self.Canvas.RenderState.set("Rendering . . .")

		for _item in self.ItemForDisable:
			_item.config(state=['disable'])

	def draw_process(self):
		time_start = time.time()
		try:
			self.FractalStruct.getPixels()

			colormap = matplotlib.cm.get_cmap(self.PaletteName.get())
			palette = []
			for i in range(self.Iterations.get()):
				rgb = colormap(i/self.Iterations.get())
				palette.insert(i,(int(rgb[0]*255),int(rgb[1]*255),int(rgb[2]*255)))

			img = Image.new("RGB", (self.FractalStruct.w, self.FractalStruct.h), "black")
			draw = ImageDraw.Draw(img)
			for p in self.FractalStruct.pixels:
				if p[2] == 0:
					draw.point((p[0], p[1]), (0,0,0))
				else:
					draw.point((p[0], p[1]), palette[p[2]])

			self.Canvas.Image = img
			photoimg = ImageTk.PhotoImage(img.resize((self.Canvas.Width, self.Canvas.Height)))
			self.Canvas.Background = photoimg
			self.Canvas.create_image(0, 0, image=self.Canvas.Background, anchor=NW)

			self.draw_process_end(True, "Render finaly for {:.2f} sec!".format(time.time()-time_start))

		except Exception as e:
			self.draw_process_end(False, "Redner Error!", error_message=str(e))

	def draw_process_end(self, succes, message, error_message=None):
		self.RenderNow = False
		self.Canvas.setup_render_end_data(succes, message, error_message=error_message)

		for _item in self.ItemForDisable:
			_item.config(state=['normal'])

	def __init__(self, mainframe, Canvas, FractalStruct):

		self.Canvas = Canvas
		self.FractalStruct = FractalStruct

		self.Formula = StringVar(value = "Z**2 + C")
		self.BuildAsJuliaEnable = IntVar()
		self.JuliaCoordX = DoubleVar(value=-0.687)
		self.JuliaCoordY = DoubleVar(value=0.312)

		self.CoordX = DoubleVar(value=-0.75)
		self.CoordY = DoubleVar()
		self.CoordZoom = DoubleVar(value=1.5)

		self.Resolution = IntVar(value=128)
		self.Iterations = IntVar(value=256)
		self.PaletteName = StringVar(value=matplotlib.pyplot.colormaps()[0])

		self.RenderNow = False
		self.RenderThread = None

		super().__init__(mainframe, width=220, relief="solid")
		self.pack(
			anchor=CENTER,
			side=LEFT,
			fill=BOTH,
			expand=False,
			padx=5,
			pady=5)

		self.grid_propagate(False)
		self.pack_propagate(False)

		self.Canvas.bind("<Control-1>", self.start_draw_after_move)

		self.create_gui()

		self.ApplyButton.config(command=self.start_draw_after_apply)
		self.ZoomInButton.config(command=self.start_draw_after_zoomIn)
		self.ZoomOutButton.config(command=self.start_draw_after_zoomOut)


class FractalCanvas(Canvas):

	def __init__(self, mainframe):
		super().__init__(mainframe, bg="gray")
		self.pack(
			anchor=CENTER,
			side=RIGHT,
			fill=BOTH,
			expand=True, 
			padx=5, 
			pady=5)

		self.ErrorMessage = None

		#### ACTUAL CANVAS SIZE HANDLER ####
		self.Width = self["width"]
		self.Height = self["height"]
		container_for_actual_size_label = StringVar(value="(0, 0)")
		def update_actual_size(event):
			self.Width = event.width
			self.Height = event.height
			container_for_actual_size_label.set(f"({self.Width}, {self.Height})")

		self.bind("<Configure>", update_actual_size)

		ttk.Label(self, textvariable=container_for_actual_size_label).pack(anchor=S, side=RIGHT)

		self.Background = None
		self.Image = None

		#### RENDER STATE VIEWER ####
		self.RenderState = StringVar(value="Ready for render.")
		
		self.RenderStateLabel = ttk.Label(self, textvariable=self.RenderState)
		self.RenderStateLabel.pack(anchor=W, side=BOTTOM)

		#### PROGRESS BAR ####
		self.RenderProgressbar = None

	def setup_render_end_data(self, succes, message, error_message=None):
		self.RenderState.set(message)
		if succes:
			self.RenderStateLabel.config(foreground="green")
		elif not succes:
			self.RenderStateLabel.config(foreground="red")
			self.ErrorMessage = ErrorMessage(self, error_message)
		