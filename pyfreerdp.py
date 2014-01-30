#!/usr/bin/python

from gi.repository import Gtk
import subprocess 

class LauncherWindow(Gtk.Window):
    """
    FreeRDP launcher window.
    """

    def __init__(self):
        """
        Initialize the window and widgets
        """

        Gtk.Window.__init__(self, title="Python FreeRDP Launcher")

        table = Gtk.Table(4, 2, False)
        self.add(table)

        label = Gtk.Label("Host and port")
        table.attach(label, 0, 1, 0, 1)

        self.addressEntry = Gtk.Entry()
        table.attach(self.addressEntry, 1, 2, 0, 1)

        label = Gtk.Label("Username")
        table.attach(label, 0, 1, 1, 2)

        self.usernameEntry = Gtk.Entry()
        table.attach(self.usernameEntry, 1, 2, 1, 2)

        label = Gtk.Label("Password")
        table.attach(label, 0, 1, 2, 3)

        self.passwordEntry = Gtk.Entry()
        self.passwordEntry.set_visibility(False)
        table.attach(self.passwordEntry, 1, 2, 2, 3)

        button = Gtk.Button(label="Connect")
        button.connect("clicked", self.connectTo)
        table.attach(button, 0, 1, 3, 4)

        button = Gtk.Button(label="Close")
        button.connect("clicked", self.closeWindow) 
        table.attach(button, 1, 2, 3, 4)

    def connectTo(self, button):
        """
        Attempt to connect using the user input.
        """

        try:
            code = -1
            command = [
                "/usr/bin/xfreerdp",
                "-K",
                "-g", "workarea",
                "--ignore-certificate",
                "--rfx",
                "--rfx-mode", "video",
                "--plugin", "cliprdr",
                "--plugin", "rdpsnd", "--data", "alsa", "--",
                "--plugin", "drdynvc", "--data", "audin", "--"]

            address = self.addressEntry.get_text()
            username = self.usernameEntry.get_text()
            password = self.passwordEntry.get_text()

            # If the username and password are present then use them.
            if username and password: 
                command.extend([
                    "-u", username,
                    "-p", "\"{0}\"".format(password)])

            # If an address is present attempt to connect.
            if address:
                command.extend([address, "&"])
                code = subprocess.call(" ".join(command), shell=True)

            # Check the return code (if any) and close on success.
            if code == 0:
                Gtk.main_quit()
        except:
            pass

    def closeWindow(self, button):
        """
        Close the window and end the program.
        """

        Gtk.main_quit()

window = LauncherWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
