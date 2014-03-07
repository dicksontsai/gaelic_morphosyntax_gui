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

	def gloss_frame(self):
		return GlossButtons(self)

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

class GlossButtons(Form):
	def __init__(self, parent, position, text1="", text2=""):
		Form.__init__(self, parent)
		self.instance = Frame(self)
		self.instance.grid(row=0)
		self.current_column = 0
		self.position = position
		self.instantiate_form(text1, text2)

	def instantiate_form(self, text1, text2):
		self.morpheme = StringVar()
		self.morpheme.set(text1)
		Entry(self.instance, textvariable=self.morpheme).grid(row=0)
		self.current_column += 1
		self.gloss = StringVar()
		self.gloss.set(text2)
		Entry(self.instance, textvariable=self.gloss).grid(row=0, column=self.current_column)
		self.current_column += 1
		Button(self.instance, text="Delete", command=self._delete).grid(row=0, column=self.current_column)
		self.current_column += 1
		Button(self.instance, text="Move up", command=self._move_up).grid(row=0, column=self.current_column)
		self.current_column += 1
		Button(self.instance, text="Move down", command=self._move_down).grid(row=0, column=self.current_column)
		self.current_column += 1

	"""
	def _delete(self):
		self.grid_forget()

	def _move_up(self, gloss_partner):


	def _move_down(self, gloss_partner):
	"""