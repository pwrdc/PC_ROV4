from threading import Thread
import tkinter as tk
import tk_tools
from collections import deque
import time


class GUI(Thread):
    def __init__(self, rpi_reference):
        self.RPI = rpi_reference
        self.start_time = time.time()
        self.main_window = tk.Tk()
        self.selected_pid = tk.StringVar()
        self.depth_pid_state = tk.StringVar()
        self.depth_pid_state.set("OFF")
        self.yaw_pid_state = tk.StringVar()
        self.yaw_pid_state.set("OFF")
        self.depth_val_log = deque(maxlen= 40)
        self.main_window.title("ROV4 simple GUI")

        self.init_topbar()
        self.init_sliders()
        self.init_guages()
        self.init_info_readings()


    def init_topbar(self):
        self.topbar_frame = tk.Frame(self.main_window)
        self.topbar_frame.grid(row=0, column=4, columnspan=6, sticky="ew")

        tk.Checkbutton(self.topbar_frame, onvalue="ON", offvalue="OFF", width=4,
                        indicatoron=False, 
                        variable=self.depth_pid_state, textvariable=self.depth_pid_state,
                        selectcolor="green", background="red",
                        command=self.depth_onoff).grid(row=0, column=1)
        tk.Radiobutton(self.topbar_frame,
                       text="depth",
                       value="depth",
                       variable=self.selected_pid,
                       command = self.mode_toggle).grid(row=0, column=2)
        tk.Radiobutton(self.topbar_frame,
                       text="yaw",
                       value="yaw",
                       variable=self.selected_pid,
                       command = self.mode_toggle).grid(row=0, column=3)
        self.selected_pid.set("depth")
        tk.Checkbutton(self.topbar_frame, onvalue="ON", offvalue="OFF", width=4,
                        indicatoron=False, 
                        variable=self.yaw_pid_state, textvariable=self.yaw_pid_state,
                        selectcolor="green", background="red",
                        command=self.yaw_onoff).grid(row=0, column=5)

    def init_sliders(self):
        self.slide_kp = tk.Scale(self.main_window,
                                 from_=0,
                                 to=300,
                                 length=400,
                                 command=self.get_kp)
        self.slide_kp.grid(column=0, row=1)
        self.slide_kp.set(50)

        self.slide_ki = tk.Scale(self.main_window,
                                 from_=0,
                                 to=2000,
                                 length=400,
                                 command=self.get_ki)
        self.slide_ki.grid(column=1, row=1)
        self.slide_ki.set(1000)

        self.slide_kd = tk.Scale(self.main_window,
                                 from_=0,
                                 to=2000,
                                 length=400,
                                 command=self.get_kd)
        self.slide_kd.grid(column=3, row=1)
        self.slide_kd.set(1465)

        self.bt = tk.Button(self.main_window, text="send parameters", command = self.send_parameters)
        self.bt.grid(column=1, row=3, columnspan=2)

    def init_guages(self):
        self.guages_frame = tk.Frame(self.main_window)
        self.guages_frame.grid(row=1, column=4)

        self.error_guage = tk_tools.Gauge(self.guages_frame,
                                          max_value=8,
                                          min_value=-8,
                                          red_low=20,
                                          red=80,
                                          yellow_low=30,
                                          yellow=70,
                                          label="error value",
                                          unit='')
        self.error_guage.set_value(0.4)
        self.pid_val_guage = tk_tools.Gauge(self.guages_frame,
                                            max_value=1.1,
                                            min_value=-1.1,
                                            red_low=20,
                                            red=80,
                                            yellow_low=30,
                                            yellow=70,
                                            label="pid value",
                                            unit='')
        self.pid_val_guage.set_value(0.1)

        self.error_guage.pack()
        self.pid_val_guage.pack()

    def init_info_readings(self):
        self.depth_graph_frame = tk.Frame(self.main_window)
        self.depth_graph_frame.grid(row=1, column=5)
        self.depth_set_point = tk.Label(self.depth_graph_frame, text="setpoint value: off")
        self.depth_set_point.pack()
        graph_title = tk.Label(self.depth_graph_frame, text="Depth value:")
        graph_title.pack()
        labelfont = ('times', 20, 'bold')
        self.depth_value_label = tk.Label(self.depth_graph_frame,
                                          text="2.01",
                                          borderwidth=2,
                                          relief="solid",
                                          font=labelfont)
        self.depth_value_label.pack()

        self.depth_graph = tk_tools.Graph(parent=self.depth_graph_frame,
                                          x_min=0,
                                          x_max=20,
                                          y_min=0.0,
                                          y_max=4.0,
                                          x_tick=2,
                                          y_tick=0.5,
                                          width=600,
                                          height=400)
        self.depth_graph.pack()

        self.yaw_frame = tk.Frame(self.main_window)
        self.yaw_frame.grid(row=1, column=6)
        self.yaw_set_point = tk.Label(self.yaw_frame, text="setpoint value: off")
        self.yaw_set_point.pack()
        tk.Label(self.yaw_frame, text="Yaw value:").pack()
        self.yaw_value_label = tk.Label(self.yaw_frame,
                                          text="180",
                                          borderwidth=2,
                                          relief="solid",
                                          font=labelfont)
        self.yaw_value_label.pack()


        self.yaw_val_guage = tk_tools.Gauge(self.yaw_frame,
                                            max_value=180,
                                            min_value=-180,
                                            red_low=20,
                                            red=80,
                                            yellow_low=30,
                                            yellow=70,
                                            label="yaw val",
                                            unit='')
        self.yaw_val_guage.set_value(30)
        self.yaw_val_guage.pack()

        # self.yaw_rotary=tk_tools.RotaryScale(self.yaw_frame,max_value=180.0).pack()

    def get_kp(self, event):
        print("kp= " + str(self.slide_kp.get() / 1000))
        self.kp = self.slide_kp.get() / 1000

    def get_ki(self, event):
        print("ki= " + str(self.slide_ki.get() / 10000))
        self.ki = self.slide_ki.get() / 10000

    def get_kd(self, event):
        print("kd= " + str(self.slide_kd.get() / 100))
        self.kd = self.slide_kd.get() / 10000

    def run(self):
        self.update_values()
        print("gui started !")
        self.main_window.mainloop()

    def read_vals(self):
        pid_vals = {"kd": 0.0, "kp": 0.0, "ki": 0.0}
        try:
            pid_vals['kp'] = float(self.kp)
            pid_vals['ki'] = float(self.ki)
            pid_vals['kd'] = float(self.kd)
            print(str(pid_vals))
            return pid_vals
        except Exception as e:
            print(e)

        return pid_vals

    def mode_toggle(self):
        if self.selected_pid.get() == "depth":
            print("selected pid: depth")
        elif self.selected_pid.get() == "yaw":
            print("selected pid: yaw")

    def depth_onoff(self):
        if self.depth_pid_state.get() == "ON":
            print("turning depth pid on...")
            setpoint = self.RPI.get_depth_set_point() # RPI get depth_setpoint
            setpoint = str(format(setpoint,'.2f'))
            self.depth_set_point.config(text="setpoint value: "+ setpoint)
        else:
            print("turning depth pid off...")
            self.depth_set_point.config(text="setpoint value: off")
            
    def yaw_onoff(self):
        if self.yaw_pid_state.get() == "ON":
            print("turning yaw pid on...")
            setpoint = self.RPI.get_yaw_set_point()  # RPI get yaw_setpoint
            setpoint = str(format(setpoint,'.1f'))
            self.yaw_set_point.config(text="setpoint value: " + setpoint)
        else:
            print("turning yaw pid off...")
            self.yaw_set_point.config(text="setpoint value: off")
     
    def send_parameters(self):
        pid_vals = self.read_vals()
        if self.selected_pid.get() == "depth":
            print("sending parameters to depth pid")
            self.RPI.pid_depth_set_params(pid_vals['kp'],
                            pid_vals['ki'],
                            pid_vals['kd'])
        elif self.selected_pid.get() == "yaw":
            print("sending parameters to yaw pid")
            self.RPI.pid_yaw_set_params(pid_vals['kp'],
                            pid_vals['ki'],
                            pid_vals['kd'])

    def update_values(self):

        if self.selected_pid.get() == "depth":
            err_val = self.RPI.get_pid_depth_error() # RPI get_pid_depth_error
            self.error_guage.set_value(err_val)
            pid_val = self.RPI.get_pid_depth_output() # RPI get_pid_depth_output
            self.pid_val_guage.set_value(pid_val)

        elif self.selected_pid.get() == "yaw":
            err_val = self.RPI.get_pid_yaw_error() # RPI get_pid_yaw_error
            self.error_guage.set_value(err_val)
            pid_val = self.RPI.get_pid_yaw_output()# RPI get_pid_yaw_output
            self.pid_val_guage.set_value(pid_val)

        depth_val = self.RPI.get_depth() #RPI get_current_depth val

        self.depth_value_label.config(text=str(format(depth_val,'.2f')))
        if round(time.time() - self.start_time, 2) > 20.0:
            self.start_time = time.time()
            self.depth_val_log.clear()
            self.depth_graph.draw_axes()
        self.depth_val_log.append((round(time.time() - self.start_time, 2),depth_val))
        self.depth_graph.plot_line(list(self.depth_val_log))

        yaw_val = self.RPI.get_yaw() #RPI get_current_yaw val

        self.yaw_value_label.config(text=str(format(yaw_val,'.1f')))
        self.yaw_val_guage.set_value(yaw_val)

        self.main_window.after(200,self.update_values)


if __name__ == "__main__":
    class VirtualRpi:
        dupa = "blada"
        
    VIRTUAL_RPI = VirtualRpi()
    gui = GUI(VIRTUAL_RPI)
    gui.run()
