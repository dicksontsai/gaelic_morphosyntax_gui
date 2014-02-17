from Tkinter import *
import tkMessageBox, tkFileDialog, tkFont
import os, fnmatch
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
#welcome_font = tkFont.Font(family='Helvetica', size='-100', weight='bold', underline=1)

class App(object):
	def __init__(self):
		self.root = Tk()
		self.root.wm_title("Gaelic MorphoSyntax Gloss Manager")

		self.top_menu = MenuBar(self.root)
		self.top_menu.grid(row=0)

		#self.canvas_scrollbar = Scrollbar(self.root)
		#self.content = Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, yscrollcommand=self.canvas_scrollbar.set)
		#self.content.pack()
		#self.content.create_text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, text="Welcome to the Gaelic\n MorphoSyntax Gloss Manager", \
			#fill="#0065BD", font=('Helvetica','-50', 'bold'))

		self.placeholder = Label(self.root, text="Placeholder")
		self.placeholder.grid(row=1, rowspan=2)

		self.welcome_label = Label(self.root, justify=CENTER, fg="#0065BD", font=('Helvetica', '-50', 'bold'), text="Welcome to the Gaelic\nMorphoSyntax Gloss Manager")
		self.welcome_label.grid(row=1, column=1, ipadx=50, ipady=50)


		self.cwd_labeltext = StringVar()
		self.cwd_labeltext.set("Your current working directory is " + os.getcwd())
		self.cwd_label = Label(self.root, textvariable=self.cwd_labeltext)
		self.cwd_label.grid(row=2, column=1)

		self.cwd_entrytext = StringVar()
		Entry(self.root, textvariable=self.cwd_entrytext).grid(row=3,column=1)
		self.buttontext = StringVar()
		self.buttontext.set("Change Working Directory")
		Button(self.root, textvariable=self.buttontext, command=self.clicked_cwd).grid(row=4, column=1)


		#self.content_window = self.content.create_window(window=)
		#self.label = Label(self.root, text="Enter your weight in pounds.")

		#self.label.pack()
		self.root.mainloop()

	def clicked_cwd(self):
		new_dir = self.cwd_entrytext.get()
		os.chdir(new_dir)
		self.cwd_labeltext.set("Your current working directory is " + new_dir)



class MenuBar(Frame):
	"""
	Special construction of the top menu that allows it to populate the Mac's top bar
	"""
	def __init__(self, parent):
		Frame.__init__(self, parent)
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
		Frame.__init__(self, parent)
#class SentenceEditor(Frame):
#class ChangeManager():

class FileSideBar(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.get_buttons()


	def get_buttons(self):
		self.buttons_list = []
		for file in os.listdir('.'):
			if fnmatch.fnmatch(file, '*.json'):
				self.buttons_list.append(SideBarButton(self, file))


class SideBarButton(Button):
	def __init__(self, parent, json_file_name):
		self.instance = Button.__init__(self, parent, text=json_file_name, command=self.__generate_event(json_file_name))

	def __generate_event(self, file_name):
		def event(self):
			pass
		return event
App()