import time
import inputs
import Pyro4
from inputs import get_gamepad
import os

fronts = ['ABS_RY', 'ABS_RX', 'ABS_X', 'ABS_Y']
back = ['ABS_Z', 'ABS_RZ']
buttons = ['BTN_TR', 'BTN_TL']
whole = fronts+back+buttons
YAW_COUNTER = 5

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


roll_n_pitch = []
yaw_con = ['ABS_RZ','ABS_Z']#BTN_TR BTN_TL
z_control = ['ABS_RX', 'ABS_Y']
acceleration = ['ABS_RY', 'ABS_X']
all_controls = roll_n_pitch+yaw_con+z_control+acceleration


def run(rpi_class_reference):
    state = PadState()
    read_state = state.read()
    if read_state == 1:
        print("No pad has been found!")
        read_state = False
    number=0
    front = 0
    right = 0
    up = 0
    roll = 0
    pitch = 0
    yaw = 0
    #yaw_counter=0
    print("I'm starting loop")
    while read_state:
        read_state = state.read()
        for item in read_state:
            #check = {'ABS_RZ':0,'ABS_Z':0,'ABS_RX':0,'ABS_Y':0,'ABS_RY':0,'ABS_X':0}
            if item in yaw_con:
                yaw = read_state[item]/100
                #check['ABS_RZ']=1
                #check['ABS_Z']=1
                if item == yaw_con[1]:
                    yaw = -0.01*read_state[item]
                    #yaw_counter=8
            elif item in acceleration:
                #yaw_counter-=1
                #if abs(yaw)>30:
                    #yaw=0
                if item == acceleration[0]:
                    #check['ABS_RY']=1
                    front = read_state[item]/100
            elif item in z_control:
                #yaw_counter-=1
                #if abs(yaw)>30:
                    #yaw=0
                if item == z_control[1]:
                    #check['ABS_Y']=1
                    up = read_state[item]/100
                else:
                    #check['ABS_RX']=1
                    right = read_state[item]/100

            
							
				

        rpi_class_reference.set_engine_driver_values(front, right, up,yaw,roll,pitch)
        #if yaw_counter<=0:
        #    yaw=0
        '''
        os.system('cls')
        print('Numer',number)
        print('Front',front)
        print('Right',right)
        print('Up',up)
        print('roll',roll)
        print('pitch',pitch)
        print('yaw',yaw)
        '''
        number+=1
        if number%YAW_COUNTER==0:
            yaw=0
        time.sleep(0.01)
    return


if __name__ == "__main__":
    class VirtualRpi:
        def movements(self, front, right, up, yaw, pitch, roll):
            print(str(front)+" "+str(right)+" "+str(up)+" "+str(yaw)+" "+str(pitch)+" "+str(roll))
    VIRTUAL_RPI = VirtualRpi()
    run(VIRTUAL_RPI)
