import zipfile
import tkMessageBox
import urllib as url

def update():
    response = tkMessageBox.askyesno("Confirmation for update", "Are you sure you want to update to the newest version?")
    if response:
            url.urlretrieve("http://github.com/dicksontsai/gaelic_morphosyntax_gui/archive/master.zip", "morphosyntax_gui.zip")
            print "Download of ZIP succeeded"
            with open('morphosyntax_gui.zip', 'r') as gui_zip:
                print "Opening"
                zipfile_object = zipfile.ZipFile(gui_zip, 'r')
                try:
                    print "Extracting"
                    zipfile_object.extractall("..")
                    print "Update installed"
                except Exception as e:
                    print e 
                    tkMessageBox.showerror("Update Failed", "Sorry, the update failed")
