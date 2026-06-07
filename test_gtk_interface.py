import sys
import gi  # Gobject Introspection - the GTK wrapper for Python


gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # Import the actual library


def on_activate(app):
    win = Gtk.ApplicationWindow(application=app)
    btn = Gtk.Button(label="Hello, World!")
    btn.connect("clicked", lambda x: win.close())
    win.set_child(btn)
    win.present()


app = Gtk.Application(application_id="org.gtk.Example")
app.connect("activate", on_activate)
app.run()


# class MyApplication(Gtk.Application):
#     def __init__(self):
#         super().__init__(application_id="com.example.MyGtkApplication")
#         GLib.set_application_name("My Gtk Application")

#     def do_activate(self):
#         window = Gtk.ApplicationWindow(application=self, title="Hello World")
#         window.present()


# app = MyApplication()
# exit_status = app.run(sys.argv)
# sys.exit(exit_status)
