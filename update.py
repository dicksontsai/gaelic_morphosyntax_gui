import zipfile
import tkMessageBox
import urllib as url

def update():
    response = tkMessageBox.askyesno("Confirmation for update", "Are you sure you want to update to the newest version?")
    if response:
        internet_zipfile = url.urlopen("http://github.com/dicksontsai/gaelic_morphosyntax_gui/archive/master.zip")
        zipfile_object = zipfile.ZipFile(internet_zipfile, 'r')
        try:
            zipfile_object.extractall(".")
        except ZipFileException: 
            tkMessageBox.showerror("Update Failed", "Sorry, the update failed")
