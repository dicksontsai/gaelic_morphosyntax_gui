from Tkinter import *
import tkMessageBox, tkFileDialog, tkFont
import os, fnmatch, json
from util import *

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
CONTENT_MIDDLE_X = 150
CONTENT_MIDDLE_Y = 150
SENTENCE_METADATA = ("sentence", "translation", "metatags")
#welcome_font = tkFont.Font(family='Helvetica', size='-100', weight='bold', underline=1)

def delete_content_frame():
	assert root.previous_frame is not None, "No frame to fall back on"
	switch_content_frames(root.previous_frame)

def switch_content_frames(new_frame=None):
	root.content.delete("self.active_frame")
	if new_frame is None:
		new_frame = root.default_frame
	assert isinstance(new_frame, Frame), "Bad input"
	root.previous_frame = root.active_frame 
	root.active_frame = new_frame
	root.content.delete(root.active_frame_window)
	root.active_frame_window = root.content.create_window((CONTENT_MIDDLE_X, CONTENT_MIDDLE_Y), window=root.active_frame, anchor=NW, tags="self.active_frame")

class App(object):
	def __init__(self):
		global root
		root = self.root = Tk()
		self.root.wm_title("Gaelic MorphoSyntax Gloss Manager")

		self.top_menu = MenuBar(self.root)
		self.top_menu.grid(row=0)
		self.root.sidebar = SideBar(self.root)

		self.root.content = Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

		self.root.content_scrollbar = Scrollbar(self.root, orient="vertical", command=self.root.content.yview)
		self.root.content.configure(yscrollcommand=self.root.content_scrollbar.set)
		self.root.content_scrollbar.grid(row=1, column=2)
		self.root.content.grid(row=1, column=1)
		#self.content.pack()
		#self.content.create_text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, text="Welcome to the Gaelic\n MorphoSyntax Gloss Manager", \
			#fill="#0065BD", font=('Helvetica','-50', 'bold'))

		#self.sidebar.grid(row=1)
		self.root.open_content_frames = {}
		self.root.active_frame = self.root.previous_frame = self.root.default_frame = self.root.open_content_frames['welcome'] = WelcomeFrame(self.root)
		self.root.active_frame_window = self.root.content.create_window((CONTENT_MIDDLE_X, CONTENT_MIDDLE_Y), window=self.root.active_frame, anchor=NW, tags="self.active_frame")
		#self.content.grid(row=1, column=1)

		self.init_bindings()

		#self.label.pack()
		self.root.mainloop()


	def init_bindings(self):
		"""These bindings define keyboard shortucts to app"""
		self.root.bind('<Control-o>', self.top_menu._openHandler)
		self.root.bind('<Control-s>', self.save_shortcut)

	def save_shortcut(self):
		if hasattr(self.root.active_frame, "save") and callable(getattr(self.root.active_frame, "save")):
			self.root.active_frame.save()
		else:
			print "No save command"

class MenuBar(Frame):
	"""
	Special construction of the top menu that allows it to populate the Mac's top bar
	"""
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.top = parent.winfo_toplevel()
		self.menuBar = Menu(self.top)
		self.top['menu'] = self.menuBar
		self.create_file_menu()

	def create_file_menu(self):
		self.fileMenu = Menu(self.menuBar)
		self.menuBar.add_cascade(label='File', menu=self.fileMenu)
		self.fileMenu.add_command(label='Open', command=self._openHandler, accelerator="Ctrl-o")

	def _openHandler(self, *e):
		selected_file = tkFileDialog.askopenfilename()
		print selected_file


class WelcomeFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent) #f
		self.parent = parent
		#self.grid(row=1, column=1)

		self.instance = Frame(self)	#f3
		self.instance.grid(row=0)

		self.welcome_label = Label(self.instance, justify=CENTER, fg="#0065BD", font=('Helvetica', '-50', 'bold'), text="Welcome to the Gaelic\nMorphoSyntax Gloss Manager")
		self.welcome_label.grid(row=0, ipadx=50, ipady=50)


		self.cwd_labeltext = StringVar()
		self.cwd_labeltext.set("Your current working directory is " + os.getcwd())
		self.cwd_label = Label(self.instance, textvariable=self.cwd_labeltext)
		self.cwd_label.grid(row=1)

		self.cwd_entrytext = StringVar()
		self.cwd_entrytext.set(os.getcwd())
		Entry(self.instance, textvariable=self.cwd_entrytext).grid(row=2)
		Button(self.instance, text="Browse", command=self.browse_wd).grid(row=2, column=1)
		self.buttontext = StringVar()
		self.buttontext.set("Change Working Directory")
		Button(self.instance, textvariable=self.buttontext, command=self.clicked_cwd).grid(row=3)

	def clicked_cwd(self, dir_name=None):
		if dir_name is not None:
			new_dir = dir_name
		else:
			new_dir = self.cwd_entrytext.get()
		os.chdir(new_dir)
		self.cwd_labeltext.set("Your current working directory is " + new_dir)
		self.cwd_entrytext.set(new_dir)
		root.sidebar.render_sidebar()

	def browse_wd(self):
		curr_dir = os.getcwd()
		new_dir = tkFileDialog.askdirectory()
		if not new_dir:
			return curr_dir
		else:
			self.clicked_cwd(new_dir)

#class SentenceEditor(Frame):
#class ChangeManager():
"""
class FileSideBar(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.grid(row=1)
		self.buttons_list = []
		self.render_sidebar()

	def render_sidebar(self):
		for button in self.buttons_list:
			button.grid_forget()
		self.__get_buttons()


	def __get_buttons(self):
		num_buttons = 0
		for file in os.listdir('.'):
			if fnmatch.fnmatch(file, '*.json'):
				button = SideBarButton(self, file)
				num_buttons += 1
				button.grid(row=num_buttons)
				self.buttons_list.append(button)

	def __str__(self):
		return "FileSideBar"
"""
class SideBar(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.grid(row=1)

		self.instance = Frame(self)
		self.instance.grid(row=0)
		self.files_list = []
		self.file_label = Label(self.instance, text="JSON files in directory")
		self.file_label.grid(row=0)
		self.new_file_button = Button(self.instance, text="Create new JSON file", command=self.new_file)
		self.new_file_button.grid(row=1)
		self.listbox = Listbox(self.instance)
		self.listbox.grid(row=2)
		self.initialize_listbox()
		self.render_sidebar()
		self.current_file = None

	def initialize_listbox(self):
		"""Bind events to the listbox"""
		@bind(self.listbox, '<<ListboxSelect>>')
		def onselect(evt):
			if self.current_file is not None:
				self.current_file.save()
			w = evt.widget
			index = int(w.curselection()[0])
			value = w.get(index)
			print 'You selected file %d: "%s"' % (index, value)
			self.current_file = FilePage(root, value)
			switch_content_frames(self.current_file)


	def render_sidebar(self):
		self.listbox.delete(0, END)
		self._get_files()


	def _get_files(self):
		for file in os.listdir('.'):
			if fnmatch.fnmatch(file, '*.json'):
				self.listbox.insert(END, file)
				self.files_list.append(file)

	def new_file(self):
		new_file_form = NewFileForm(root)
		switch_content_frames(new_file_form)

	def add_file_to_sidebar(self, file_name):
		assert ".json" in file_name, "This file is not in JSON format"
		self.listbox.insert(END, file_name)
		self.files_list.append(file_name)

	"""
	def __str__(self):
		return "SideBar"
	"""
"""
class SideBarButton(Button):
	def __init__(self, parent, json_file_name):
		Button.__init__(self, parent, text=json_file_name, command=self.__generate_event(json_file_name))
		self.parent = parent
		self.file = json_file_name

	def __generate_event(self, file_name):
		def event(self):
			if file_name not in root.open_content_frames:
				root.open_content_frames[file_name] = FilePage(root, file_name)###
			switch_content_frames(root.content, root.open_content_frames[file_name])
		return event

	def __str__(self):
		return "SideBarButton: " + self.file
"""

class FilePage(Frame):
	""" Displays the frame for each json file"""
	def __init__(self, parent, json_file_name):
		Frame.__init__(self, parent)
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
		new_sentence_form = NewSentenceForm(root, self)
		switch_content_frames(new_sentence_form)

	def new_sentence_display(self, sentence_obj):
		self.sentences.append(sentence_obj)
		if hasattr(self, "empty_label"):
			self.empty_label.grid_forget()
		self.sentence_index += 1
		button_index = self.sentence_index
		self.sentence_button_text.append(self.compute_preview(sentence_obj, button_index))
		button = Button(self.instance, textvariable=self.sentence_button_text[button_index], justify=LEFT, command=lambda: self.edit_sentence(button_index))
		button.grid(row=self.current_row)
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
		button_text.set(str(button_index) + ") " + "\n".join(previews))
		return button_text

	def edit_sentence(self, sentence_index):
		# TODO: Make sure sentence editor marks the original sentence dirty and moves new sentence into the dictionary when saved
		edit_form = SentenceEditor(root, sentence_index, self)
		switch_content_frames(edit_form)

	def save(self):
		"""
		Saves any changes made to the FilePage
		"""
		file_to_write = open(self.file, 'w')
		file_to_write.write(json.dumps(self.json))
		print self.file + " is saved"

	"""
	def __str__(self):
		return "FilePage: " + self.file
	"""

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

class NewFileForm(Form):
	def __init__(self, parent):
		Form.__init__(self, parent)
		self.create_form()

	def create_form(self):
		self.entries = {}
		self.entries["filename"] = self.input("Filename:")
		self.entries["book"] = self.input("Book:")
		self.entries["chapter"] = self.input("Chapter:")
		self.entries["author"] = self.input("Author:")
		self.cancel_button(self._cancel)
		self.save_button(self._generate_file, "Generate new JSON file")

	def _cancel(self):
		delete_content_frame()

	def _generate_file(self):
		file_name = self.entries["filename"].get()
		if ".json" not in file_name:
			file_name = file_name + ".json"
		new_file = open(file_name, "w")
		json_object = {entry: self.entries[entry].get() for entry in ("book", "chapter", "author")}
		json_object["sentences"] = []
		new_file.write(json.dumps(json_object))
		root.sidebar.add_file_to_sidebar(file_name)
		delete_content_frame()

class SentenceForm(Form):
	"""A form that deals with sentences"""
	def sentence_metadata_input(self):
		self.entries = {}
		self.entries["sentence"] = self.textarea("Whole sentence.")
		self.entries["translation"] = self.textarea("Translation: ")
		self.entries["metatags"] = self.textarea("Metatags: ")

	def get_responses(self):
		self.responses = {}
		for key, value in self.entries.items():
			if isinstance(value, Text):

				self.responses[key] = value.get(0.0, END)
				self.responses[key] = self.responses[key].strip("\n")
			else: #This value is the glosses input
				self.responses[key] = [[a.get(), b.get().strip("\n")] for a, b in value]

	def fill_responses(self, sentence_obj):
		for word in SENTENCE_METADATA:
			self.entries[word].insert(END, sentence_obj[word])

class NewSentenceForm(SentenceForm):
	def __init__(self, parent, file_page):
		Form.__init__(self, parent)
		responses = self.create_metadata_form()
		self.file_page = file_page

	def create_metadata_form(self):
		self.sentence_metadata_input()
		self.cancel_button(self._cancel)
		self.save_button(self._generate_sentence, "Create the sentence")

	def _cancel(self):
		assert isinstance(root.previous_frame, FilePage), "Not a file page"
		delete_content_frame()

	def _generate_sentence(self):
		self.get_responses()
		glosses = self.responses["sentence"].strip(".,")
		self.responses["glosses"] = [[gloss, "^"] for gloss in glosses.split('+')]
		self.file_page.new_sentence_display(self.responses)
		print "Index passed in: " + str(self.file_page.sentence_index) + " and actual length is " + str(len(self.file_page.sentences))
		switch_content_frames(SentenceEditor(root, self.file_page.sentence_index, self.file_page))

class SentenceEditor(SentenceForm):
	def __init__(self, parent, sentence_index, file_page):
		Form.__init__(self, parent)
		self.file_page = file_page
		self.sentence_index = sentence_index
		self.create_sentence_form(self.file_page.sentences[sentence_index])

	def create_sentence_form(self, sentence_obj):
		self.sentence_metadata_input()
		self.entries["glosses"] = []
		for gloss in sentence_obj["glosses"]:
			self.entries["glosses"].append(self.input_pair(gloss[0], gloss[1]))
		self.fill_responses(sentence_obj)
		self.cancel_button(self._cancel)
		self.save_button(lambda: self.save(remain=True), "Save and stay", column=2)
		self.save_button(lambda: self.save(remain=False), "Save and exit", column=3)

	def _cancel(self):
		switch_content_frames(self.file_page)

	def save(self, remain=True):
		self.get_responses()
		self.file_page.sentences[self.sentence_index] = self.responses
		self.file_page.save()
		if not remain:
			self.recompute_preview()
			switch_content_frames(self.file_page)

	def recompute_preview(self):
		button_text = self.file_page.sentence_button_text[self.sentence_index]
		sentence_obj = self.file_page.sentences[self.sentence_index]
		self.file_page.compute_preview(sentence_obj, self.sentence_index, button_text)

app = App()

"""
My notes:
- Sentences will be represented as JSON object with:
	- "sentence": Whole sentence
	- "glosses": List of [morpheme, gloss]
		- TODO: Easier to store combined tags separately or together?
	- "translation": Literal Translation
	- "metatags": List of metatags
"""
