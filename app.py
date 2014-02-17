from Tkinter import *
import tkMessageBox, tkFileDialog, tkFont
import os, fnmatch, json
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
#welcome_font = tkFont.Font(family='Helvetica', size='-100', weight='bold', underline=1)

def switch_content_frames(frame1, frame2):
	frame1.grid_forget()
	frame2.grid(row=1, column=1)
	root.content = frame2

class App(object):
	def __init__(self):
		global root
		root = self.root = Tk()
		self.root.wm_title("Gaelic MorphoSyntax Gloss Manager")

		self.top_menu = MenuBar(self.root)
		self.top_menu.grid(row=0)

		#self.canvas_scrollbar = Scrollbar(self.root)
		#self.content = Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, yscrollcommand=self.canvas_scrollbar.set)
		#self.content.pack()
		#self.content.create_text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, text="Welcome to the Gaelic\n MorphoSyntax Gloss Manager", \
			#fill="#0065BD", font=('Helvetica','-50', 'bold'))

		self.root.sidebar = FileSideBar(self.root)
		#self.sidebar.grid(row=1)
		self.root.open_content_frames = {}
		self.root.content = self.root.open_content_frames['welcome'] = WelcomeFrame(self.root)
		#self.content.grid(row=1, column=1)



		#self.content_window = self.content.create_window(window=)
		#self.label = Label(self.root, text="Enter your weight in pounds.")

		#self.label.pack()
		self.root.mainloop()



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
		self.fileMenu.add_command(label='Open', command=self.__openHandler)

	def __openHandler(self):
		selected_file = tkFileDialog.askopenfilename()
		print selected_file


class WelcomeFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent) #f
		self.parent = parent
		self.grid(row=1, column=1)

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
		self.buttontext = StringVar()
		self.buttontext.set("Change Working Directory")
		Button(self.instance, textvariable=self.buttontext, command=self.clicked_cwd).grid(row=3)

	def clicked_cwd(self):
		new_dir = self.cwd_entrytext.get()
		os.chdir(new_dir)
		self.cwd_labeltext.set("Your current working directory is " + new_dir)
		self.cwd_entrytext.set(new_dir)
		root.sidebar.render_sidebar()

#class SentenceEditor(Frame):
#class ChangeManager():

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

class SideBarButton(Button):
	def __init__(self, parent, json_file_name):
		Button.__init__(self, parent, text=json_file_name, command=self.__generate_event(json_file_name))
		self.parent = parent

	def __generate_event(self, file_name):
		def event(self):
			if file_name not in root.open_content_frames:
				root.open_content_frames[file_name] = FilePage(root, file_name)###
			switch_content_frames(root.content, root.open_content_frames[file_name])
		return event

class FilePage(Frame):
	""" Displays the frame for each json file"""
	def __init__(self, parent, json_file_name):
		Frame.__init__(self, parent)
		
		try:
			sentences = json.load(open(json_file_name))
		except ValueError:
			print "Empty JSON file"
			return



app = App()