import time
import inputs
import Pyro4
from inputs import get_gamepad
import os


def run(rpi_class_reference):

    #dive
    rpi_class_reference.movements(0, 0, -50,0,0,0)
    time.sleep(1)
    #front
    rpi_class_reference.movements(40, 0, 0, 0, 0, 0)
    time.sleep(5)
    #rotate
    rpi_class_reference.movements(0, 0, 0, 30, 0, 0)
    time.sleep(0.5)
    #front
    rpi_class_reference.movements(40, 0, 0, 0, 0, 0)
    time.sleep(5)
    #surface
    rpi_class_reference.movements(0, 0, 50,0,0,0)
    time.sleep(2)
    rpi_class_reference.movements(0, 0, 0,0,0,0)



if __name__ == "__main__":
    class VirtualRpi:
        def movements(self, front, right, up, yaw, pitch, roll):
            print(str(front)+" "+str(right)+" "+str(up)+" "+str(yaw)+" "+str(pitch)+" "+str(roll))
    VIRTUAL_RPI = VirtualRpi()
    run(VIRTUAL_RPI)
