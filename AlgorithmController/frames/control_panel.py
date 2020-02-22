import tkinter as tk
from tkinter import ttk
import tkinter.messagebox


from frames.controlable_frame import ControlFrame


class ControlPanel(tk.Frame):
    """
    Main frame with all sliders
    To control algorithms
    """

    sliders = []
    values = []
    stones = []

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.sliders_container = ControlFrame(self)
        self.sliders_container.grid(row=0, column=0, sticky='nsew')

        self.buttons_container = ttk.Frame(self)
        self.buttons_container.place(relx=0.5, rely=0.8, anchor='center')

        # create reset and save button
        self.create_buttons()

    def create_widgets(self) -> None:
        """
        Creating all sliders for changing parameters
        :return:
        """
        for i, stone in enumerate(self.stones):
            self.create_slider(stone.task,
                               stone.algorithm,
                               stone.attribute,
                               stone.value, i)

    def create_slider(self, task: str, algorithm: str,
                      attribute: str, value: int, column: int) -> None:
        """
        Create slider
        :param task: task name
        :param algorithm: algorithm name
        :param attribute: attribute name
        :param value: value of attribute
        :param column: column to put
        :return:
        """
        # container of slider
        container = ttk.Frame(
            self.sliders_container.container,
            style='SliderFrame.TFrame'
        )
        container.grid(row=0, column=column, sticky='nse', padx=7)

        # labels
        label_task = ttk.Label(
            container,
            text=task.capitalize()
        )
        label_task.grid(row=0, pady=(10, 0))
        label_algorithm = ttk.Label(
            container,
            text=algorithm.capitalize()
        )
        label_algorithm.grid(row=1, pady=(5, 5))
        label_attribute = ttk.Label(
            container,
            text=attribute,
            font=('TkDefaultFont', 8)
        )
        label_attribute.grid(row=2, pady=(2, 2))

        # variable - important(as fuck)
        variable = tk.DoubleVar(value=value)
        self.values.append(variable)

        # adjusting value to dimension
        to_value = 0
        resolution = 1
        if value < 0.1:
            to_value = value * 1000
            resolution = 0.01
        elif 0.1 < value < 1:
            to_value = value * 100
            resolution = 0.1
        else:
            to_value = value * 10

        # scale bar
        scale_bar = tk.Scale(
            container,
            from_=0,
            to=to_value,
            variable=variable,
            showvalue=0,
            resolution=resolution
        )
        scale_bar.grid(row=3, padx=(5, 5))

        self.sliders.append(scale_bar)

        # show value
        entry = tk.Entry(
            container,
            textvariable=variable,
            width=8
        )
        entry.grid(row=4)

    def create_buttons(self) -> None:
        """
        Create buttons to control model
        :return:
        """
        reset_button = ttk.Button(
            self.buttons_container,
            text='Reset settings',
            command=lambda: self.reset_values()
        )
        reset_button.grid(row=0, column=0, sticky='w')

        save_button = ttk.Button(
            self.buttons_container,
            text='Save settings',
            command=lambda: self.save_values()
        )
        save_button.grid(row=0, column=1, sticky='e')

    def reset_values(self) -> None:
        """
        Resets all values
        :return:
        """
        for i in range(len(self.values)):
            self.values[i].set(self.stones[i].get_value())

    def save_values(self) -> None:
        """
        Save all values to stone and json
        :return:
        """
        for i in range(len(self.values)):
            self.stones[i].set_value(self.values[i].get())
        self.controller.save_stones(self.stones)
        self.controller.save_json()

    def use_json(self) -> None:
        """
        Creates all widgets if gets json
        :return:
        """
        if self.try_get_json():
            self.stones = self.controller.get_stones()
            self.create_widgets()

    def try_get_json(self) -> bool:
        """
        Gets json and create widgets if true
        :return:
        """
        success = False
        try:
            self.controller.get_json()
            success = True
        except Exception as e:
            tkinter.messagebox.showinfo('Error!', e)
        return success
