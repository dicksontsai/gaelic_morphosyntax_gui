from Tkinter import *

from form import *
from util import *

class SentenceForm(Form):
	"""A form that deals with sentences"""
	def sentence_metadata_input(self):
		self.entries = {}
		self.entries["sentence"] = self.textarea("Whole sentence. Remember to add + between each word.")
		self.entries["translation"] = self.textarea("Translation: ")
		self.entries["my_translation"] = self.checkbox("My translation")
		self.entries["metatags"] = self.textarea("Metatags: ")
		self.entries["page"] = self.input("Page: Use decimal for precision (i.e. 5.1 = pg. 5 top, 5.9 = pg. 5 bottom")

	def get_responses(self):
		self.responses = {}
		for key, value in self.entries.items():
			if isinstance(value, Text):
				self.responses[key] = value.get(0.0, END)
				self.responses[key] = self.responses[key].strip("\n")
			elif key == "page" or key=="my_translation":
				self.responses[key] = str(self.entries[key].get())
			else: #This value is the glosses input
				self.responses[key] = [[gloss.morpheme.get(), gloss.gloss.get().strip("\n")] for gloss in value if not gloss.dirty]

	def fill_responses(self, sentence_obj):
		for word in SENTENCE_METADATA:
			if word == "page" or word=="my_translation": #This is for new sentence attributes
				if word in sentence_obj:
					self.entries[word].set(sentence_obj[word])
				continue
			self.entries[word].insert(END, sentence_obj[word])

	def add_gloss_button(self, position, offset):
		button = Button(self.instance, text="Add gloss")
		button.position = position
		button.configure(command=self.add_gloss_function(button, offset))
		button.grid(row=self.current_row)
		self.current_row += 1

	def add_gloss_function(self, button, offset):
		def add_gloss():
			button.grid_forget()
			self.entries["glosses"].append(self.gloss_frame(button.position, offset))
			button.position += 1
			button.grid(row=self.current_row)
			self.current_row += 1
		return add_gloss

class NewSentenceForm(SentenceForm):
	def __init__(self, parent, file_page):
		Form.__init__(self, parent)
		responses = self.create_metadata_form()
		self.file_page = file_page
		self.root = parent
		#self.bind("<Enter>", self._generate_sentence)

	def create_metadata_form(self):
		self.sentence_metadata_input()
		self.cancel_button(self._cancel)
		self.save_button(self._generate_sentence, "Create the sentence")

	def _cancel(self):
		assert isinstance(self.root.previous_frame, FilePage), "Not a file page"
		self.root.delete_content_frame()

	def _generate_sentence(self):
		self.get_responses()
		glosses = self.responses["sentence"].strip(".,")
		self.responses["glosses"] = [[gloss, "^"] for gloss in glosses.split('+')]
		self.responses["sentence"] = self.responses["sentence"].replace("+", " ")
		#print "Index passed in: " + str(self.file_page.sentence_index) + " and actual length is " + str(len(self.file_page.sentences))
		self.root.switch_content_frames(SentenceEditor(self.root, self.file_page.sentence_index+1, self.file_page, self.responses))

class SentenceEditor(SentenceForm):
	def __init__(self, parent, sentence_index, file_page, new_sentence=None):
		Form.__init__(self, parent)
		self.file_page = file_page
		self.sentence_index = sentence_index
		self.new_sentence = new_sentence
		self.root = parent
		if new_sentence:
			target_sentence = new_sentence
		else:
			target_sentence = self.file_page.sentences[sentence_index]
		self.create_sentence_form(target_sentence)
		#self.bind("<Enter>", lambda event: self.save(remain=False))

	def create_sentence_form(self, sentence_obj):
		self.sentence_metadata_input()
		self.entries["glosses"] = []
		index_counter = 0
		offset = self.current_row
		for gloss in sentence_obj["glosses"]:
		#	self.entries["glosses"].append(self.input_pair(gloss[0], gloss[1]))
			self.entries["glosses"].append(self.gloss_frame(index_counter, offset, gloss[0], gloss[1]))
			index_counter += 1
		#print "gloss button" + str(self.current_row)
		self.add_gloss_button(index_counter, offset)
		#print [gloss.gloss.get() for gloss in self.entries["glosses"]]
		self.fill_responses(sentence_obj)
		self.cancel_button(self._cancel)
		self.save_button(lambda: self.save(remain=True), "Save and stay", column=2)
		self.save_button(lambda: self.save(remain=False), "Save and exit", column=3)

	def _cancel(self):
		self.root.switch_content_frames(self.file_page)

	def save(self, remain=True):
		self.get_responses()
		if self.new_sentence:
			self.file_page.new_sentence_display(self.responses, add_to_sentences=True)
		print str(self.sentence_index)
		self.file_page.sentences[self.sentence_index] = self.responses

		self.file_page.save()
		if not remain:
			self.recompute_preview()
			self.root.switch_content_frames(self.file_page)

	def recompute_preview(self):
		button_text = self.file_page.sentence_button_text[self.sentence_index]
		sentence_obj = self.file_page.sentences[self.sentence_index]
		self.file_page.compute_preview(sentence_obj, self.sentence_index, button_text)

