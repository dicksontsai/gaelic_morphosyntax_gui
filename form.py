from Tkinter import *
import tkMessageBox

class Form(Frame):
	""" A class inspired by HTML """
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.grid(row=1)
		self.instance = Frame(self)
		self.instance.grid(row=0)
		self.current_row = 0

	def checkbox(self, text):
		value = IntVar()
		Checkbutton(self.instance, text=text, variable=value).grid(row=self.current_row)
		self.current_row += 1
		return value

	def input(self, text):
		"""Sets up the Label and Entry widgets and then returns a pointer to the StringVar"""
		Label(self.instance, text=text, justify=LEFT).grid(row=self.current_row)
		self.current_row += 1
		entry_text = StringVar()
		Entry(self.instance, textvariable=entry_text).grid(row=self.current_row)
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

	def gloss_frame(self, position, offset, morpheme="", gloss=""):
		gloss_frame = GlossButtons(self.instance, position, offset, morpheme, gloss)
		#print "gloss frame: " + str(self.current_row)
		gloss_frame.grid(row=self.current_row)
		self.current_row += 1
		return gloss_frame

	def textarea(self, text, height=15):
		Label(self.instance, text=text, justify=LEFT).grid(row=self.current_row)
		self.current_row += 1
		text_area = Text(self.instance, height=height) # Use .get(1, END) 
		text_area.grid(row=self.current_row)
		self.current_row += 1
		text_area.bind("<Tab>", self._focus_next_window)
		return text_area

	def cancel_button(self, cancel_action, text="Cancel"):
		#print self.current_row
		Button(self.instance, text=text, command=cancel_action).grid(row=self.current_row, column=1)

	def save_button(self, save_action, text="Save", column=2):
		Button(self.instance, text=text, command=save_action).grid(row=self.current_row, column=column)

	def _focus_next_window(self, event):
		widget = event.widget.tk_focusNext()
		widget.focus()
		return "break"

class GlossButtons(Form):
	def __init__(self, parent, position, offset, text1, text2):
		Form.__init__(self, parent)
		self.instance = Frame(self)
		self.instance.grid(row=0)
		self.current_column = 0
		self.position = position # Position in the list
		self.offset = offset # Remember that we are gridding with the Text widgets as well
		self.parent = parent
		self.dirty = False
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

	
	def _delete(self):
		"""I should add a dirty-gloss identifier here"""
		self.grid_forget()
		self.dirty = True

	def _move_up(self):
		gloss_list = self.parent.master.entries["glosses"]
		offset = self.offset
		try:
			if self.position <= 0:
				raise IndexError
			gloss_partner = gloss_list[self.position-1]
			self.grid_forget()
			gloss_partner.grid_forget()
			gloss_partner.grid(row=self.position+offset)
			gloss_partner.position = self.position
			self.position -= 1
			self.grid(row=self.position+offset)
			gloss_list[self.position], gloss_list[self.position + 1] = self, gloss_partner
		except IndexError:
			tkMessageBox.showerror("Invalid Move Up", "Cannot move this pair up.")

	def _move_down(self):
		gloss_list = self.parent.master.entries["glosses"]
		offset = self.offset
		try:
			if self.position >= len(gloss_list):
				raise IndexError

			gloss_partner = gloss_list[self.position + 1]
			self.grid_forget()
			gloss_partner.grid_forget()
			gloss_partner.position = self.position
			#print gloss_partner.position
			gloss_partner.grid(row=self.position + offset)
			self.position += 1
			self.grid(row=self.position + offset)
			gloss_list[self.position], gloss_list[self.position - 1] = self, gloss_partner
		except IndexError:
			tkMessageBox.showerror("Invalid Move Down", "Cannot move this pair down.")