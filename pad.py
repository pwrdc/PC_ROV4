import time
import inputs
import Pyro4
from inputs import get_gamepad

fronts = ['ABS_RY', 'ABS_RX', 'ABS_X', 'ABS_Y']
back = ['ABS_Z', 'ABS_RZ']
buttons = ['BTN_TR', 'BTN_TL']
whole = fronts+back+buttons


class PadState(object):
    def __init__(self):
        self.dict = {}

    def order(self):
        for item in fronts:
            if item in self.dict:
                self.dict[item] = int(round(100*self.dict[item]/32767, 0))
        for item in back:
            if item in self.dict:
                self.dict[item] = int(round(100*self.dict[item]/255, 0))

    def read(self):
        while 1:
            try:
                events = get_gamepad()
            except inputs.UnpluggedError:
                return 1

            for event in events:
                if event.state:
                    for item in whole:
                        if event.code == item:
                            self.dict.clear()
                            self.dict[event.code] = event.state
                            self.order()
                            return self.dict


roll_n_pitch = ['ABS_RY', 'ABS_RX']
yaw_con = ['BTN_TR', 'BTN_TL']
z_control = ['ABS_X', 'ABS_Y']
acceleration = ['ABS_RZ', 'ABS_Z']
all_controls = roll_n_pitch+yaw_con+z_control+acceleration


def main():
    uri = input("uri: ").strip()
    movement = Pyro4.Proxy(uri)

    state = PadState()
    read_state = state.read()
    if read_state == 1:
        print("No pad has been found!")
        read_state = False

    while read_state:
        front = 0
        right = 0
        up = 0
        roll = 0
        pitch = 0
        yaw = 0

        read_state = state.read()
        for item in read_state:
            if item in yaw_con:
                yaw = 100
                if item == yaw_con[1]:
                    yaw = -100
            elif item in roll_n_pitch:
                if item == roll_n_pitch[0]:
                    roll = read_state[item]
                else:
                    pitch = read_state[item]
            elif item in acceleration:
                if item == acceleration[0]:
                    front = read_state[item]
                else:
                    front = (-1)*read_state[item]
            elif item in z_control:
                if item == z_control[1]:
                    up = read_state[item]
                else:
                    right = read_state[item]

        movement.set_lin_velocity(front, right, up)
        movement.set_ang_velocity(roll, pitch, yaw)
        time.sleep(0.05)
    return


if __name__ == "__main__":
    main()
