import time
from collections import defaultdict
from xbox360controller import Xbox360Controller
import Pyro4
from threading import Thread

### gui prototype
import tkinter as tk

### gui
from gui import GUI

class Display(Thread):
    def __init__(self):
        self.kp = 0.5
        self.ki= 0.000145
        self.kd = 1000
        self.root = tk.Tk()
        self.root.title("pid controll")

        self.slide1 = tk.Scale(self.root, from_=0, to=500, length=500,
                            command=self.get_kp)
        self.slide1.pack( side = "left")
        self.slide1.set(50)

        self.slide2 = tk.Scale(self.root, from_=0, to=200, length=500,
                            command=self.get_kd)
        self.slide2.pack( side = "left")
        self.slide2.set(1465)

        self.slide3 = tk.Scale(self.root, from_=0, to=2000, length=500,
                            command=self.get_ki)
        self.slide3.pack( side = "left")
        self.slide3.set(1000)

    def get_kp(self, event):
        print("kp= " + str(self.slide1.get()/100))
        self.kp = self.slide1.get()/100
        

    
    def get_ki(self, event):
        print("ki= " + str(self.slide3.get()/10000))
        self.ki = self.slide3.get()/10000
    
    def get_kd(self, event):
        print("kd= " + str(self.slide2.get()/100))
        self.kd = self.slide2.get()/100

    def run(self):
        print("small gui started")
        self.root.mainloop()

    def read_vals(self):
        pid_vals = {"kd":0.0, "kp":0.0, "ki":0.0}
        try:
            pid_vals['kp'] = float(self.kp)
            pid_vals['ki'] = float(self.ki)
            pid_vals['kd'] = float(self.kd)
            print("set" + str(pid_vals))
        except Exception as e:
            print(e)

        return pid_vals
### gui prototype

def read_pid_vals():
    raw = input("Enter pid vals: kp, ki, kd\ne.g.'1.0 4.5 3.5'\n")
    lst = raw.split(" ")
    pid_vals = {"kd":0.0, "kp":0.0, "ki":0.0}
    try:
        pid_vals['kp'] = float(lst[0])
        pid_vals['ki'] = float(lst[1])
        pid_vals['kd'] = float(lst[2])
        print("set" + str(pid_vals))
    except Exception as e:
        print(e)

    return pid_vals

class X360controler:
    VAR_DICT = {'x_par': 1, 'y_par': 1, 'z_par': 1, 'yaw_par': 1}  # exponential functions steepness parameters

    yaw_change = 5
    depth_change = 0.1
    numberOfEngines = 0
    numberOfValues = 4
    run = True
    left_stick = [0, 0]
    right_stick = [0, 0]
    left_trigger = 0.0
    right_trigger = 0.0
    deadzone = 0.05
    engines = numberOfValues * [0]  # x_vel, y_vel, z_vel, yaw_vel
    #engines = 10 * [0.0]
    swiatla = 0
    obslugaDanych = None
    buttons = {'A': False,
               'B': False,
               'X': False,
               'Y': False,
               'LB': False,
               'RB': False,
               'LS': False,
               'RS': False,
               'back': False,
               'start': False,
               'mode': False,
               'DU': False,
               'DD': False,
               'DL': False,
               'DR': False}
    switches = {'A': False,
                'B': False,
                'X': False,
                'Y': False,
                'LB': False,
                'RB': False,
                'LS': False,
                'RS': False,
                'back': False,
                'start': False,
                'mode': False,
                'DU': False,
                'DD': False,
                'DL': False,
                'DR': False}
    PID_DEPTH_ON = False
    PID_YAW_ON = False
    EXPONENTIAL_MODE_ON = True
    EXP_FUN_BASE = 101 ** (1 / 100)  # exponential function base
    EXP_FUN_LINMOD = 0  # linear modifier
    EXP_FUN_C = 1  # exponential function steepness coefficient
    """ 
    buttonsReactions: 'Releasedbutton_a','Releasedbutton_b','Releasedbutton_x','Releasedbutton_y','Releasedbutton_trigger_l','Releasedbutton_trigger_r': self._rb,
    ,'Releasedbutton_thumb_l','Releasedbutton_thumb_r','Releasedbutton_select','Releasedbutton_start': self._start,'Releasedbutton_mode',
    'Releasedbutton_back'
    'Pressedbutton_a','Pressedbutton_b','Pressedbutton_x','Pressedbutton_y','Pressedbutton_trigger_l','Pressedbutton_trigger_r': self._rb,
    ,'Pressedbutton_thumb_l','Pressedbutton_thumb_r','Pressedbutton_select','Pressedbutton_start': self._start,'Pressedbutton_mode',
    'Pressedbutton_back'
    """

    def __init__(self, rpi_reference):
        
        ### gui prototype
        self.gui = GUI(rpi_reference)
        print('init')
        ### gui prototype

        self.RPI = rpi_reference

        self.buttonReactions = defaultdict(lambda: None, {'a':'b'})
        #self.buttonReactions = {'Pressedbutton_a':self.RPI.pid_turn_on,
        #                        'Pressedbutton_b':self.RPI.pid.turn_off,
        #                        'Pressedbutton_y':self.RPI.pid_hold_depth}

        #buttonReactions= defaultdict(lambda: None,{'a':'b'})

        # FOR PID
        self.pid_vals = {"kd":0.0, "kp":0.0, "ki":0.0}
        #END PID

    def adjust_deadzone(self, value, dzone):
        if abs(value) > dzone:
            return (value - sign(value) * dzone) / (1 - dzone)
        else:
            return 0

    # PAD ACTIONS
    def a(self):
        # button_a
        self.buttons['A'] = True
        self.switches['A'] = not self.switches['A']
        print('A')
        #if self.buttonReactions['PressedButton_a'] != None:
        #    self.buttonReactions['PressedButton_a']()
        #self.RPI.pid_set_params(self.pid_vals['kp'],
        #                        self.pid_vals['ki'],
        #                        self.pid_vals['kd'])
        self.RPI.pid_hold_yaw()

    def _a(self):
        # button_a
        self.buttons['A'] = False
        print('_A')
        #if self.buttonReactions['Releasedbutton_a'] != None:
        #    self.buttonReactions['Releasedbutton_a']()

    def b(self):
        # button_b
        self.buttons['B'] = True
        self.switches['B'] = not self.switches['B']
        print('B')

        self._run_in_thread(self.RPI.pid_depth_turn_off)
        print("PID turn off")

        #if self.buttonReactions['PressedButton_b'] != None:
        #    self.buttonReactions['PressedButton_b']()

    def _b(self):
        # button_b
        self.buttons['B'] = False
        print('_B')
        #if self.buttonReactions['Releasedbutton_b'] != None:
        #    self.buttonReactions['Releasedbutton_b']()

    def x(self):
        # button_x
        self.buttons['X'] = True
        self.switches['X'] = not self.switches['X']
        print('X')

        if not self.PID_DEPTH_ON:
            self._run_in_thread(self.RPI.pid_depth_turn_on)
            self._run_in_thread(self.RPI.pid_hold_depth)
            self.PID_DEPTH_ON = True
            print("PID depth turn on")
        else:
            self._run_in_thread(self.RPI.pid_depth_turn_off)
            self.PID_DEPTH_ON = False
            print("PID depth turn off")
        #if self.buttonReactions['PressedButton_x'] != None:
        #    self.buttonReactions['PressedButton_x']()

    def _x(self):
        # button_x
        self.buttons['X'] = False
        print('_X')
        #if self.buttonReactions['Releasedbutton_x'] != None:
        #    self.buttonReactions['Releasedbutton_x']()

    def y(self):
        # button_y
        self.buttons['Y'] = True
        self.switches['Y'] = not self.switches['Y']
        print('Y')

        if not self.PID_YAW_ON:
            self._run_in_thread(self.RPI.pid_yaw_turn_on)
            self._run_in_thread(self.RPI.pid_hold_yaw)
            self.PID_YAW_ON = True
            print("PID yaw turn on")
        else:
            self._run_in_thread(self.RPI.pid_yaw_turn_off)
            self.PID_YAW_ON = False
            print("PID yaw turn off")

        #if self.buttonReactions['PressedButton_y'] != None:
        #    self.buttonReactions['PressedButton_y']()

    def _y(self):
        # button_y
        self.buttons['Y'] = False
        print('_Y')
        #if self.buttonReactions['Releasedbutton_y'] != None:
        #    self.buttonReactions['Releasedbutton_y']()

    def lb(self):
        # button_trigger_l
        self.buttons['LB'] = True
        self.switches['LB'] = not self.switches['LB']
        print('LB')

    def _lb(self):
        # button_trigger_l
        self.buttons['LB'] = False
        print('_LB')

    def rb(self):
        # button_trigger_r
        self.buttons['RB'] = True
        self.switches['RB'] = not self.switches['RB']
        print('RB')

    def _rb(self):
        # button_trigger_r
        self.buttons['RB'] = False
        print('_RB')

    def ls(self):
        # button_thumb_l
        self.buttons['LS'] = True
        self.switches['LS'] = not self.switches['LS']
        print('LS')
        #self.cur_mode = not self.cur_mode
        #print('Mov mode: {}'.format(self.cur_mode))

    def _ls(self):
        # button_thumb_l
        self.buttons['LS'] = False
        print('_LS')

    def rs(self):
        # button_thumb_r
        self.buttons['RS'] = True
        self.switches['RS'] = not self.switches['RS']
        print('RS')
        #self.cur_precision = not self.cur_precision
        #print('Precision mode: {}'.format(self.cur_precision))
        inp = input()
        print(inp)

    def _rs(self):
        # button_thumb_r
        self.buttons['RS'] = False
        print('_RS')

    def back(self):
        # button_select
        self.buttons['back'] = True
        self.switches['back'] = not self.switches['back']
        print('back')
        self.RPI.pid_yaw_turn_off()

    def _back(self):
        # button_select
        self.buttons['back'] = False
        print('_back')
        if self.buttonReactions['Releasedbutton_back'] != None:
            self.buttonReactions['Releasedbutton_back']()

    # press to open parameter modification terminal
    def start(self):
        # button_start
        self.buttons['start'] = True
        self.switches['start'] = not self.switches['start']
        print('start')
        if self.buttonReactions['PressedButton_start'] != None:
            self.buttonReactions['PressedButton_start']()
        ### gui prototype
        # self.pid_vals=read_pid_vals()
        #self.pid_vals = self.gui.read_vals()
        ### gui prototype
        if not self.take_input():
            print("take_input: invalid input.")

    def _start(self):
        # button_start
        self.buttons['start'] = False
        print('_start')
        if self.buttonReactions['ReleasedButton_y'] != None:
            self.buttonReactions['ReleasedButton_y']()

    def mode(self):
        # button_mode
        self.buttons['mode'] = True
        self.switches['mode'] = not self.switches['mode']
        print('mode')
        self.run = False
        if self.buttonReactions['Pressedbutton_mode'] != None:
            self.buttonReactions['Pressedbutton_mode']()

    def _mode(self):
        # button_mode
        self.buttons['mode'] = False
        print('_mode')
        if self.buttonReactions['Releasedbutton_mode'] != None:
            self.buttonReactions['Releasedbutton_mode']()

    def left(self, axis):
        # axis_l
        self.left_stick[0] = self.adjust_deadzone(axis.x, 3 * self.deadzone)
        self.left_stick[1] = -self.adjust_deadzone(axis.y, 3 * self.deadzone)

    def right(self, axis):
        # axis_r
        self.right_stick[0] = self.adjust_deadzone(axis.x, 3 * self.deadzone)
        self.right_stick[1] = -self.adjust_deadzone(axis.y, 3 * self.deadzone)

    def hat(self, axis):
        # hat
        if axis.x == 1:
            self.buttons['DR'] = True
            self.buttons['DL'] = False
            self.switches['DR'] = not self.switches['DR']
            value = self.RPI.get_yaw_set_point() + self.yaw_change
            self._run_in_thread(self.RPI.pid_set_yaw(value))
            print("PID yaw set to ", value)
        elif axis.x == -1:
            self.buttons['DL'] = True
            self.buttons['DR'] = False
            self.switches['DL'] = not self.switches['DL']
            value = self.RPI.get_yaw_set_point() - self.yaw_change
            self._run_in_thread(self.RPI.pid_set_yaw(value))
            print("PID yaw set to ", value)
        else:
            self.buttons['DR'] = False
            self.buttons['DL'] = False
        if axis.y == 1:
            self.buttons['DU'] = True
            self.buttons['DD'] = False
            self.switches['DU'] = not self.switches['DU']
            value = self.RPI.get_depth_set_point() + self.depth_change
            self._run_in_thread(self.RPI.pid_set_depth(value))
            print("PID depth set to ", value)
        elif axis.y == -1:
            self.buttons['DD'] = True
            self.buttons['DU'] = False
            self.switches['DD'] = not self.switches['DD']
            value = self.RPI.get_depth_set_point() - self.depth_change
            self._run_in_thread(self.RPI.pid_set_depth(value))
            print("PID depth set to ", value)
        else:
            self.buttons['DD'] = False
            self.buttons['DU'] = False

    def lt(self, axis):
        # trigger_l
        self.left_trigger = axis.value

    def rt(self, axis):
        # trigger_r
        self.right_trigger = axis.value

    def on_pressed(self, button):
        options = {'button_a': self.a,
                   'button_b': self.b,
                   'button_x': self.x,
                   'button_y': self.y,
                   'button_trigger_l': self.lb,
                   'button_trigger_r': self.rb,
                   'button_thumb_l': self.ls,
                   'button_thumb_r': self.rs,
                   'button_select': self.back,
                   'button_start': self.start,
                   'button_mode': self.mode}
        options[button.name]()

    def on_released(self, button):
        options = {'button_a': self._a,
                   'button_b': self._b,
                   'button_x': self._x,
                   'button_y': self._y,
                   'button_trigger_l': self._lb,
                   'button_trigger_r': self._rb,
                   'button_thumb_l': self._ls,
                   'button_thumb_r': self._rs,
                   'button_select': self._back,
                   'button_start': self._start,
                   'button_mode': self._mode}
        options[button.name]()

    def on_moved(self, axis):
        options = {'axis_l': self.left,
                   'axis_r': self.right,
                   'hat': self.hat,
                   'trigger_l': self.lt,
                   'trigger_r': self.rt}
        options[axis.name](axis)

    # STEERING FUNCTIONS
    def steering(self):
        x_vel = 100 * self.right_stick[1]
        y_vel = 100 * self.right_stick[0]
        z_vel = 100 * (self.right_trigger - self.left_trigger)
        yaw_vel = 100 * self.left_stick[0]

        # modifying steering values from linear to exponential
        x_vel = self.lin2exp(x_vel, self.VAR_DICT['x_par'])
        y_vel = self.lin2exp(y_vel, self.VAR_DICT['y_par'])
        z_vel = self.lin2exp(z_vel, self.VAR_DICT['z_par'])
        yaw_vel = self.lin2exp(yaw_vel, self.VAR_DICT['yaw_par'])

        self.engines[0] = int(x_vel)
        self.engines[1] = int(y_vel)
        self.engines[2] = int(z_vel)
        self.engines[3] = int(yaw_vel)

    def cart2coord(self, x_coord, y_coord, z_coord, o_coord, a_coord, t_coord):  # to add inverse kinematics!
        pair1 = 1 * x_coord
        pair2 = 1 * y_coord
        pair3 = 1 * z_coord
        pair4 = 1 * o_coord
        pair5 = 1 * a_coord
        pair6 = 1 * t_coord
        return [pair1, pair2, pair3, pair4, pair5, pair6]

    def Start(self):

        with Xbox360Controller(0, axis_threshold=self.deadzone) as controller:
            # BUTTONS
            controller.button_a.when_pressed = self.on_pressed  # A
            controller.button_a.when_released = self.on_released
            controller.button_b.when_pressed = self.on_pressed  # B
            controller.button_b.when_released = self.on_released
            controller.button_x.when_pressed = self.on_pressed  # X
            controller.button_x.when_released = self.on_released
            controller.button_y.when_pressed = self.on_pressed  # Y
            controller.button_y.when_released = self.on_released
            controller.button_trigger_l.when_pressed = self.on_pressed  # LB
            controller.button_trigger_l.when_released = self.on_released
            controller.button_trigger_r.when_pressed = self.on_pressed  # RB
            controller.button_trigger_r.when_released = self.on_released
            controller.button_thumb_l.when_pressed = self.on_pressed  # LS
            controller.button_thumb_l.when_released = self.on_released
            controller.button_thumb_r.when_pressed = self.on_pressed  # RS
            controller.button_thumb_r.when_released = self.on_released
            controller.button_select.when_pressed = self.on_pressed  # back
            controller.button_select.when_released = self.on_released
            controller.button_start.when_pressed = self.on_pressed  # start
            controller.button_start.when_released = self.on_released
            controller.button_mode.when_pressed = self.on_pressed  # mode
            controller.button_mode.when_released = self.on_released
            # AXES
            controller.axis_l.when_moved = self.on_moved  # left
            controller.axis_r.when_moved = self.on_moved  # right
            controller.hat.when_moved = self.on_moved  # hat
            controller.trigger_l.when_moved = self.on_moved  # LT
            controller.trigger_r.when_moved = self.on_moved  # RT
            # The Loop
            counter =0
            while self.run:
                self.steering()
                time.sleep(0.005)
                counter+=1
                if counter==20:
                    counter=0
                    #print(self.engines)

                for e in self.engines:
                    if e>50:
                        e=-50
                    if e<50:
                        e =-50
                try:
                    self.RPI.set_engine_driver_values(self.engines[0]/100, self.engines[1]/100, self.engines[2]/100,0, 0, self.engines[3]/100)
                except Exception:
                    pass

    def _run_in_thread(self, func):
        thread = Thread(target=func)
        thread.start()

    def take_input(self):
        """
        input format: command variable value
        commands: set
        variables: x_par, y_par, z_par, yaw_par
        """
        print("Input command in format: command variable value")
        input_string = input()
        input_list = input_string.split(' ')
        if len(input_list) != 3:
            return False
        command_input = input_list[0]
        var_input = input_list[1]
        try:
            val_input = float(input_list[2])
        except:
            return False
        if command_input == 'set':
            if self.set_value(var_input, val_input):
                return True
        return False

    def set_value(self, var, val):
        try:
            self.VAR_DICT[var] = val
            return True
        except:
            return False

    def lin2exp(self, val, c=1):
        """
        transforms value of linear function y = x [-100, 100] to it's (almost) exponential equivalent
        (modified by a linear part)
        :param val: input value
        :param c: function coefficient - larger makes function steeper;
        c=1 - pure exponential function - see steering_function.png
        c=0 - linear function (no transformation)
        :return: transformed value in range [-100, 100]
        """
        if c == 0:
            return val

        if c != self.EXP_FUN_C:  # optimization - linear modifier value computed only when changed
            self.EXP_FUN_LINMOD = 100 / (101 ** c - 1)  # linear modifier
        return sign(val) * (self.EXP_FUN_BASE ** (c * abs(val)) - 1) * self.EXP_FUN_LINMOD


def sign(val):
    if val != 0:
        return val / abs(val)
    else:
        return 0


if __name__ == '__main__':
    class VirtualRpi:
        def set_engine_driver_values(self, front, right, up, yaw, pitch, roll):
            pass
            print(str(front)+" "+str(right)+" "+str(up)+" "+str(yaw)+" "+str(pitch)+" "+str(roll))

        def pid_turn_on(self):
            print("PID turn on")

        def pid_turn_off(self):
            print("PID turn off")

        def pid_hold_depth(self):
            print("PID hold depth")

        def pid_set_params(self, kp, ki, kd):
            print("pid_set_params: kp: "+str(kp)+" ki: "+str(ki)+" kd: "+str(kd))



    VIRTUAL_RPI = VirtualRpi()
    pad = X360controler(VIRTUAL_RPI)
    thread = Thread(target=pad.Start)
    thread.start()
    pad.gui.run()
    #pad.Start()
