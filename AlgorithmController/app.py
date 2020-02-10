import tkinter as tk
from tkinter import ttk


from components import JsonManager, Connection, XAVIER_PATH, SELF_PATH
from frames import LoginPanel, ControlPanel
from styles import style_config

# all frames in application
FRAMES = {
    'login_panel': LoginPanel,
    'control_panel': ControlPanel
}


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        JsonManager.create_file(SELF_PATH)
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        style_config(self)

        self.title('Algorithm Controller')
        self.geometry('500x300')
        self.resizable(False, False)

        # main container for frames
        container = ttk.Frame(self)
        container.grid()

        # getting connection
        self.connection = Connection()

        # all frames in app
        self.frames = dict()
        for key, frame in FRAMES.items():
            self.frames[key] = frame(container, self)
            self.frames[key].grid(row=0, column=0, sticky='nsew')

        self.show_frame('login_panel')

    def destroy(self):
        """
        Overriding 'destroy' to removing 'temp.json' at the end of session
        :return:
        """
        JsonManager.remove_file(SELF_PATH)
        super().destroy()

    def show_frame(self, page: str) -> None:
        """
        Switch between of frames in self.frames
        :param page: name of page
        :return:
        """
        frame = self.frames[page]
        frame.tkraise()

    def connect(self, user: str, password: str) -> bool:
        """
        Try to connect if it's successful, return True to login page
        :param user: username@host
        :param password: password
        :return:
        """
        success = self.connection.connect_to_server(user, password)
        if success:
            success = self.get_json()
        return success

    def get_json(self) -> bool:
        """
        Creating json manager, if it's successful, return True
        :return:
        """
        self.connection.load_json()
        self.json_manager = JsonManager(XAVIER_PATH)
        success = self.json_manager.open_json()
        return success

    def get_stones(self):
        """
        Gets json_manager stones
        :return:
        """
        return self.json_manager.get_stones()

    def save_stones(self, stones) -> None:
        """
        Change json object
        :param stones:
        :return:
        """
        self.json_manager.save_json(stones)
