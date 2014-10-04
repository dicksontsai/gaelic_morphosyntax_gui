Morphosyntax GUI
===============

A Python-based GUI that makes managing JSON files containing sentence glossing data easier.

Installation
------------
* Clone this repo. To do so, make sure you have `git` installed on your computer.
* Move secrets.txt into the folder. It should be a JSON object containing the `app_secret`, and `app_key`.
    {"app_secret": "...", "app_key": "..."}
* Make sure you have `pip` installed on your machine.
* In the dropbox_sdk folder, run `pip install dropbox`.
* The app should now be ready.

Configuration
-------------
Currently, there are two options and they are editable in `config.py`.
* Language
* Dictionary website: the website that you can open while in the app using a keyboard shortcut.

Ideal usage
----------
* Dedicate a folder on your computer just for storing data. This app is best used on that folder.
* Each JSON file represents a single chapter of a book. Within each chapter, you can add sentences to it.
* A sentence consists of:
  - Sentence - the text of the sentence itself
  - Metatags - additional linguistic information about the sentence that does not pertain to a particular morpheme
  - Glosses - A list of [morpheme, gloss] pairs. These can be different from the sentences/translations.
  - Translation - Translation of the sentence, according to the native speaker.
  - My Translation - Whether the researcher makes own translation (vs. other translator)
  - Page - the page in which the sentence is located in the chapter. Decimal representation helps sort the sentences
    - Example: for page 5, 5.1 represents beginning of page, 5.5 middle, 5.9 end. The third sentence from the beginning of the page can be 5.13

Other features
------------
* Ctrl-w - Write JSON files to Dropbox. To do so, register this app and then create a `secrets.txt` folder in the same directory as the program, as described above.
  - When you authenticate, your access code will be saved in that file as well. From then on, you will not need to re-authenticate
  - Files with the same name will be overwritten.
