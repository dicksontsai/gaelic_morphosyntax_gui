from Tkinter import *
import tkMessageBox
import json, os
from util import *
from sentence_handler import *

class FilePage(Frame):
	""" Displays the frame for each json file"""
	def __init__(self, root, json_file_name):
		Frame.__init__(self, root)
		self.root = root
		self.grid(row=1)
		self.instance = Frame(self)
		self.instance.grid(row=0)
		self.sentence_index = -1
		self.current_row = 0
		Button(self.instance, text="Add new sentence", command=self._new_sentence).grid(row=self.current_row, column=1)
		self.current_row += 1
		self.file = json_file_name
		self.sentence_button_text = []
		self.load_sentences()

	def load_sentences(self):
		try:
			self.json = json.load(open(self.file))
			self.sentences = self.json["sentences"]
			if len(self.sentences) == 0:
				self.empty_label = Label(self.instance, text="This JSON file is empty. Please click the button to add a new sentence", justify=CENTER)
				self.empty_label.grid(row=1)
				return
			counter, length = 0, len(self.sentences)
			while counter < length:
				self.new_sentence_display(self.sentences[counter])
				counter += 1
			return
		except ValueError:
			print "Invalid JSON file"
			return

	def _new_sentence(self):
		#root.previous_frame = self
		new_sentence_form = NewSentenceForm(self.root, self)
		self.root.switch_content_frames(new_sentence_form)

	def new_sentence_display(self, sentence_obj, add_to_sentences=False):
		if add_to_sentences:
			self.sentences.append(sentence_obj)
		if hasattr(self, "empty_label"):
			self.empty_label.grid_forget()
		self.sentence_index += 1
		button_index = self.sentence_index
		self.sentence_button_text.append(self.compute_preview(sentence_obj, button_index))
		button = Button(self.instance, textvariable=self.sentence_button_text[button_index], justify=LEFT, command=lambda: self.edit_sentence(button_index))
		button.grid(row=self.current_row)
		deleter = Button(self.instance, text="Delete", command=lambda:self.delete_sentence(button_index))
		deleter.grid(row=self.current_row, column=1)
		self.current_row += 1

	def compute_preview(self, sentence_obj, button_index, button_text=None):
		if button_text is None:
			button_text = StringVar()
		previews = []
		for key in SENTENCE_METADATA:
			entry = sentence_obj[key]
			if key == "sentence":
				entry = entry.replace("+", " ")
			if len(entry) > 30:
				entry = entry[:30] + "..."
			previews.append(entry)
		previews.append("Missing glosses: " + str(reduce(lambda x, y: x + int("^" in y), sentence_obj["glosses"], 0)))
		display_string = str(button_index) + ") " + "\n".join(previews)
		button_text.set(display_string)
		return button_text

	def edit_sentence(self, sentence_index):
		# TODO: Make sure sentence editor marks the original sentence dirty and moves new sentence into the dictionary when saved
		"""Currently duplicates sentences"""
		edit_form = SentenceEditor(self.root, sentence_index, self)
		self.root.switch_content_frames(edit_form)

	def save(self):
		"""
		Saves any changes made to the FilePage
		"""
		os.remove(self.file)
		file_to_write = open(self.file, 'w')
		#print self.sentences
		a = json.dumps(self.json)
		#print a
		file_to_write.write(a)
		print self.file + " is saved"

	def delete_sentence(self, sentence_index):
		"""Currently does not work"""
		if not tkMessageBox.askyesno("Delete sentence prompt", "Delete sentence " + str(sentence_index) + "?"):
			return
		print(sentence_index)
		a = self.sentences.pop(sentence_index)
		print(a)
		self.save()
		self.root.active_frame = self.root.previous_frame
		self.root.switch_content_frames(FilePage(self.root, self.file))



	"""
	def __str__(self):
		return "FilePage: " + self.file
	"""