import form
from Tkinter import *
import dropbox
import webbrowser
import json, os, fnmatch
import tkMessageBox

class DropboxManager():
    """ Displays the frame for each json file"""
    def __init__(self, root, previous_frame, command):
        self.root = root
        self.previous_frame = previous_frame
        self.command = command

    def read_secrets(self):
        """ Read from secrets.txt """
        try:
            with open('secrets.txt') as secrets_file:
                secrets = json.load(secrets_file)
                if "app_key" not in secrets or "app_secret" not in secrets:
                    print "App key and app secret not filled out"
                    return -1
                if "access_code" not in secrets:
                    access_code_form = AccessCodeForm(self.root, self, self.previous_frame)
                    self.get_access_code(secrets)
                    self.root.switch_content_frames(access_code_form)
                    return 0
                self.access_code = secrets["access_code"]
                return 1
        except Exception as e:
            print e
            return -2

    def get_access_code(self, secrets):
        self.flow = dropbox.client.DropboxOAuth2FlowNoRedirect(secrets["app_key"], secrets["app_secret"])
        authorize_url = self.flow.start()
        webbrowser.open(authorize_url)

    def request(self):
        result = self.read_secrets()
        if result > 0:
            self.dispatch()
        elif result == -1:
            tkMessageBox.showerror("Missing app key and/or app secret", "Please check your secrets.txt file for your app key and app secret.")
        elif result == -2:
            tkMessageBox.showerror("Missing secrets.txt file", "Please make sure to provide a secrets.txt file with an app key and app secret.")

    def dispatch(self):
        """Put possible interaction commands here."""
        assert len(self.command) != 0, "No command passed in"
        if self.command == "save":
            return self.write_to_dropbox()

    def write_to_dropbox(self):
        assert hasattr(self, "access_code"), "Somehow skipped the access code step"
        client = dropbox.client.DropboxClient(self.access_code)
        for json_file in os.listdir('.'):
            if fnmatch.fnmatch(json_file, '*.json'):
                with open(json_file, 'r') as f:
                    client.put_file("/" + json_file, f, overwrite=True)
        tkMessageBox.showinfo("The files are successfully uploaded to Dropbox.")

def main():
    if APP_KEY == '' or APP_SECRET == '':
        exit("You need to set your APP_KEY and APP_SECRET!")
    authorize_url = flow.start()
    webbrowser.open(authorize_url)
    print 'Copy the authorization code'
    code = raw_input('>> ').strip()
    access_token, user_id = flow.finish(code)
    ## Make sure to store the access token somewhere
    ## For reference, my access code is gOfuLaE0lPIAAAAAAAAAEMtLloMwBWgGc4BgBBOKBGc
    client = dropbox.client.DropboxClient(access_token)
    print 'linked account: ', client.account_info()

class AccessCodeForm(form.Form):
    def __init__(self, root, manager, previous_frame):
        form.Form.__init__(self, root)
        self.root = root
        self.manager = manager
        self.previous_frame = previous_frame
        self.current_row = 0
        self.form_setup()

    def form_setup(self):
        intro_text = "If you are seeing this paragraph, it must be your first time connecting to Dropbox. \nYou will be redirected to the website to log in. Please place the resulting access code below."
        Label(self.instance, text=intro_text, justify=LEFT).grid(row=self.current_row)
        self.current_row += 1
        access_code = self.input("Access code:")
        self.save_button(self.save_action_function(access_code))

    def save_action_function(self, access_code_container):
        def save_action():
            access_code = access_code_container.get()
            if len(access_code) == 0:
                return
            self.manager.access_code, user_id = self.manager.flow.finish(access_code)
            with open('secrets.txt', 'r') as secrets_file:
                secrets = json.load(secrets_file)
                secrets["access_code"] = self.manager.access_code
                with open('secrets.txt', 'w') as secrets_to_write:
                    json.dump(secrets, secrets_to_write)
            self.manager.write_to_dropbox()
            self.root.switch_content_frames(self.previous_frame)
        return save_action


class SimpleFrame(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.grid(row=1)
        self.instance = Frame(self)
        self.instance.grid(row=0)
        self.current_row = 0
        Button(self.instance, text="Add new sentence").grid(row=self.current_row, column=1)
