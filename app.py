from Tkinter import *
import tkMessageBox, tkFileDialog, tkFont
from PIL import Image
import os, fnmatch, json
from util import *
import httplib
from filepage import FilePage
from form import Form
import types

#welcome_font = tkFont.Font(family='Helvetica', size='-100', weight='bold', underline=1)

def delete_content_frame(self):
	assert self.previous_frame is not None, "No frame to fall back on"
	self.switch_content_frames(self.previous_frame)

def switch_content_frames(self, new_frame=None):
	self.content.delete("self.active_frame")
	if new_frame is None:
		new_frame = self.default_frame
	assert isinstance(new_frame, Frame), "Bad input"
	self.previous_frame = self.active_frame 
	self.active_frame = new_frame
	self.content.delete(self.active_frame_window)
	self.active_frame_window = self.content.create_window((CONTENT_MIDDLE_X, CONTENT_MIDDLE_Y), window=self.active_frame, anchor=NW, tags="self.active_frame")

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
		DeveloperBox(self.root).grid(row=2)

		#self.root.delete_content_frame = delete_content_frame
		#self.root.switch_content_frames	= switch_content_frames
		self.root.delete_content_frame = types.MethodType(delete_content_frame, self.root, self.root.__class__)
		self.root.switch_content_frames	= types.MethodType(switch_content_frames, self.root, self.root.__class__)
		#self.sidebar.grid(row=1)
		self.root.active_frame = self.root.previous_frame = self.root.default_frame = WelcomeFrame(self.root)
		self.root.active_frame_window = self.root.content.create_window((CONTENT_MIDDLE_X, CONTENT_MIDDLE_Y), window=self.root.active_frame, anchor=NW, tags="self.active_frame")
		#self.content.grid(row=1, column=1)

		self.init_bindings()

		#self.label.pack()
		self.root.mainloop()


	def init_bindings(self):
		"""These bindings define keyboard shortucts to app"""
		self.root.bind('<Control-o>', self.top_menu._openHandler)
		self.root.bind('<Control-s>', self.save_shortcut)

	def save_shortcut(self, *e):
		if hasattr(self.root.active_frame, "save") and callable(getattr(self.root.active_frame, "save")):
			self.root.active_frame.save()
		else:
			print "No save command"

class DeveloperBox(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.instance = Frame(self)
		self.instance.grid(row=0)
		self.code_box = Text(self.instance)
		self.code_box.grid(row=0)
		self.run_button = Button(self.instance, text="Run code", command=self.execute_code)
		self.run_button.grid(row=0, column=1)

	def execute_code(self):
		command = self.code_box.get(0.0, END)
		exec(command)
		self.code_box.delete(0.0, END)
"""
class OnlineDictionary(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.instance = Frame(self)
		self.instance.grid(row=0)
		self.initiate_entry()

	def initiate_entry(self):
		self.lookup_word = StringVar()
		self.lookup_entry = Label(self.instance, textvariable=self.lookup_word)
		self.lookup_entry.grid(row=0)
		self.lookup_button = Button(self.instance, text="Search", command=self.parse_response)
		self.lookup_button.grid(row=0, column=1)

	def parse_response(self):
		conn = httplib.HTTPConnection("")
"""

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
			self.parent.switch_content_frames(self.current_file)


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
		root.switch_content_frames(new_file_form)

	def add_file_to_sidebar(self, file_name):
		assert ".json" in file_name, "This file is not in JSON format"
		self.listbox.insert(END, file_name)
		self.files_list.append(file_name)

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
