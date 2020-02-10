from tkinter import ttk
import tkinter as tk


class ControlFrame(tk.Frame):
    """
    Scrollable frame for containing widgets
    ALL COMPONENTS HAVE TO BE PUT IN SELF.CONTAINER
    """
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.container = ttk.Frame(canvas)

        self.container.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.container, anchor="nw")

        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=1, column=0, sticky='ew')
