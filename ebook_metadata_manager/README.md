#### Ebook metadata manager


This is a simple learning project: a Linux script, written in Python, that will:

1. scan through a directory containing ebooks
2. parse files metadata, where available
3. rename each file according to a predefined schema: <book_name> - <author_name>

The script generates a decent logfile that can tell whether everything went according to plan, and which files where not processed if any.


#### Development notes
Gnome:
How to install development library for PyGObject: [see HERE](https://pygobject.gnome.org/getting_started.html#ubuntu-getting-started)


# TO-DO:


* Port the script to Gnome (it's currently only compatible with the KDE kdialog file picker)
* Port the script to Windows (no one's gonna use it anyway, but it'd be a good exercise)
* Add some failsafe for the disgraced scenario where the user selected the wrong directory (i.e. one that contains files other than ebooks), or at least test the script more thoroughly to make sure that that will not cause any damage
* make this into a Python package
* **Aspirational** : add a GUI component that can let the user choose which file types should be processed
