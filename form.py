from Tkinter import *

class Form(Frame):
	""" A class inspired by HTML """
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.grid(row=1)
		self.instance = Frame(self)
		self.instance.grid(row=0)
		self.current_row = 0
	
	def input(self, text):
		"""Sets up the Label and Entry widgets and then returns a pointer to the StringVar"""
		Label(self.instance, text=text, justify=LEFT).grid(row=self.current_row)
		entry_text = StringVar()
		Entry(self.instance, textvariable=entry_text).grid(row=self.current_row, column=1)
		self.current_row += 1
		return entry_text

	def input_pair(self, text1="", text2=""):
		"""Sets up two pairs of input that are next to each other"""
		entry_1 = StringVar()
		entry_1.set(text1)
		Entry(self.instance, textvariable=entry_1).grid(row=self.current_row)
		entry_2 = StringVar()
		entry_2.set(text2)
		Entry(self.instance, textvariable=entry_2).grid(row=self.current_row, column=1)
		self.current_row += 1
		return entry_1, entry_2

	def textarea(self, text, height=15):
		Label(self.instance, text=text, justify=LEFT).grid(row=self.current_row)
		self.current_row += 1
		text_area = Text(self.instance, height=height) # Use .get(1, END) 
		text_area.grid(row=self.current_row)
		self.current_row += 1
		return text_area

	def cancel_button(self, cancel_action, text="Cancel"):
		Button(self.instance, text=text, command=cancel_action).grid(row=self.current_row, column=1)

	def save_button(self, save_action, text="Save", column=2):
		Button(self.instance, text=text, command=save_action).grid(row=self.current_row, column=column)