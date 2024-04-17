from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class ErrorMessage(ttk.Frame):
	def __init__(self, mainframe, error_message="Error: None"):
		super().__init__(mainframe)

		self.FullMessage = error_message
		self.ErrorMessagePreview = None
		if len(error_message) >= 45:
			self.ErrorMessagePreview = "Error: " + error_message[0:35] + "..."
		else:
			self.ErrorMessagePreview = "Error: " + self.FullMessage

		ttk.Label(self, text=self.ErrorMessagePreview).pack(anchor=CENTER, side=LEFT, fill=X)
		ttk.Button(self, text="Show more", command=self.show_more_error).pack(anchor=CENTER, side=LEFT, fill=X)
		ttk.Button(self, text="Close", command=self.destroy).pack(anchor=CENTER, side=LEFT)

		self.pack(anchor=W, side=BOTTOM)

	def show_more_error(self):
		messagebox.showerror("Error log", self.FullMessage)