import tkinter as tk
from tkinter import ttk
import tkinter.messagebox


class LoginPanel(ttk.Frame):

    """
    Login panel for application
    """

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.controller = controller

        # variables for user, password and if password has to be visible
        self.user = tk.StringVar(value='nvidia@192.168.103')
        self.password = tk.StringVar(value='nvidia')
        self.is_password_visible = tk.BooleanVar()

        # main container of this page
        settings_container = ttk.Frame(
            self,
            padding=(30, 15, 30, 15)
        )
        settings_container.place(relx=0.5, rely=0.5, anchor='center')
        settings_container.columnconfigure((0, 1, 2), weight=1)

        # widgets
        self.login_label = ttk.Label(
            settings_container,
            text='Adress: '
        )
        self.login_label.grid(columnspan=2, sticky='ew')

        self.login_entry = tk.Entry(
            settings_container,
            textvariable=self.user,
            width=25
        )
        self.login_entry.grid(columnspan=2, sticky='ew')

        self.password_label = ttk.Label(
            settings_container,
            text='Password: '
        )
        self.password_label.grid(columnspan=2, sticky='ew')

        self.password_entry = tk.Entry(
            settings_container,
            textvariable=self.password,
            show='*',
            width=30
        )
        self.password_entry.grid(sticky='ew')

        # changing if password has to be visible or not
        self.show_password_check = ttk.Checkbutton(
            settings_container,
            text='Show password',
            onvalue=True,
            offvalue=False,
            variable=self.is_password_visible,
            command=self.show_hide_password
        )
        self.show_password_check.grid(column=0, sticky='w')

        # button to connect
        self.connect_button = ttk.Button(
            settings_container,
            text='Connect',
            command=self.try_connection
        )
        self.connect_button.grid(column=0, sticky='ew')

    def show_hide_password(self) -> None:
        """
        Changing password_entry 'show' property
        :return
        """
        if self.is_password_visible.get():
            self.password_entry['show'] = ''
        else:
            self.password_entry['show'] = '*'

    def try_connection(self) -> None:
        """
        Send user and password to main controller
        If connection is established go to control page,
        Else ask for user and password again
        :return:
        """
        if self.controller.connect(
            self.user.get(),
            self.password.get()
        ):
            self.controller.frames['control_panel'].use_json()
            self.controller.show_frame('control_panel')
        else:
            tkinter.messagebox.showinfo('Error', 'Connection failed, try again.')