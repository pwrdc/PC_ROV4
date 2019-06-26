import time
from collections import defaultdict
from xbox360controller import Xbox360Controller
import Pyro4
from threading import Thread


class X360controler:
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

    """ 
    buttonsReactions: 'Releasedbutton_a','Releasedbutton_b','Releasedbutton_x','Releasedbutton_y','Releasedbutton_trigger_l','Releasedbutton_trigger_r': self._rb,
    ,'Releasedbutton_thumb_l','Releasedbutton_thumb_r','Releasedbutton_select','Releasedbutton_start': self._start,'Releasedbutton_mode',
    'Releasedbutton_back'
    'Pressedbutton_a','Pressedbutton_b','Pressedbutton_x','Pressedbutton_y','Pressedbutton_trigger_l','Pressedbutton_trigger_r': self._rb,
    ,'Pressedbutton_thumb_l','Pressedbutton_thumb_r','Pressedbutton_select','Pressedbutton_start': self._start,'Pressedbutton_mode',
    'Pressedbutton_back'
    """

    def __init__(self, rpi_reference):
        self.RPI = rpi_reference

        self.buttonReactions = defaultdict(lambda: None, {'a':'b'})
        #self.buttonReactions = {'Pressedbutton_a':self.RPI.pid_turn_on,
        #                        'Pressedbutton_b':self.RPI.pid.turn_off,
        #                        'Pressedbutton_y':self.RPI.pid_hold_depth}

        #buttonReactions= defaultdict(lambda: None,{'a':'b'})
        
    def sign(self, val):
        if val != 0:
            return val / abs(val)
        else:
            return 0

    def adjust_deadzone(self, value, dzone):
        if abs(value) > dzone:
            return (value - self.sign(value) * dzone) / (1 - dzone)
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

        self._run_in_thread(self.RPI.pid_turn_off)
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

        self._run_in_thread(self.RPI.pid_turn_on)
        print("PID turn on")

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

        self._run_in_thread(self.RPI.pid_hold_depth)
        print("PID hold depth")

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
        self.cur_mode = not self.cur_mode
        print('Mov mode: {}'.format(self.cur_mode))

    def _ls(self):
        # button_thumb_l
        self.buttons['LS'] = False
        print('_LS')

    def rs(self):
        # button_thumb_r
        self.buttons['RS'] = True
        self.switches['RS'] = not self.switches['RS']
        print('RS')
        self.cur_precision = not self.cur_precision
        print('Precision mode: {}'.format(self.cur_precision))

    def _rs(self):
        # button_thumb_r
        self.buttons['RS'] = False
        print('_RS')

    def back(self):
        # button_select
        self.buttons['back'] = True
        self.switches['back'] = not self.switches['back']
        print('back')
        if self.buttonReactions['Pressedbutton_back'] != None:
            self.buttonReactions['Pressedbutton_back']()

    def _back(self):
        # button_select
        self.buttons['back'] = False
        print('_back')
        if self.buttonReactions['Releasedbutton_back'] != None:
            self.buttonReactions['Releasedbutton_back']()

    def start(self):
        # button_start
        self.buttons['start'] = True
        self.switches['start'] = not self.switches['start']
        print('start')
        if self.buttonReactions['PressedButton_start'] != None:
            self.buttonReactions['PressedButton_start']()

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
        elif axis.x == -1:
            self.buttons['DL'] = True
            self.buttons['DR'] = False
            self.switches['DL'] = not self.switches['DL']
        else:
            self.buttons['DR'] = False
            self.buttons['DL'] = False
        if axis.y == 1:
            self.buttons['DU'] = True
            self.buttons['DD'] = False
            self.switches['DU'] = not self.switches['DU']
        elif axis.y == -1:
            self.buttons['DD'] = True
            self.buttons['DU'] = False
            self.switches['DD'] = not self.switches['DD']
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
        x_vel = 100 * (self.right_trigger - self.left_trigger)
        y_vel = 100 * self.right_stick[0]
        z_vel = 100 * self.right_stick[1]
        yaw_vel = 100 * self.left_stick[0]
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
                    print(self.engines)

                for e in self.engines:
                    if e>50:
                        e=-50
                    if e<50:
                        e =-50
                try:
                    self.RPI.set_engine_driver_values(self.engines[0]/100, self.engines[1]/100, self.engines[2]/100,self.engines[3]/100, 0, 0)
                except Exception:
                    pass

    def _run_in_thread(self, func):
        thread = Thread(target=func)
        thread.start()

if __name__ == '__main__':
    class VirtualRpi:
        def movements(self, front, right, up, yaw, pitch, roll):
            print(str(front)+" "+str(right)+" "+str(up)+" "+str(yaw)+" "+str(pitch)+" "+str(roll))
    VIRTUAL_RPI = VirtualRpi()
    pad = X360controler(VIRTUAL_RPI)
    pad.Start()
