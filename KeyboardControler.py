import time
from threading import Thread
from pynput.keyboard import Key, Listener
import Pyro4


class KeybordControler:
    """
    to close press 'k'
    """
    numberOfEngines = 0
    numberOfValues = 4
    run = True

    swiatla = 0
    obslugaDanych = None

    speed = 0

    up =     'w'
    down =   's'
    left =   'a'
    right =  'd'
    rotateR ='q'
    rotateL ='e'
    goUp =   'r'
    goDown = 'f'

    close = 'k'

    OsX = 0.0
    OsY = 0.0
    OsZ = 0.0
    rotate = 0.0

    def __init__(self, rpi_reference):
        self.RPI = rpi_reference

    def on_press(self, key):
        """
        function call if any key is pressed
        """
        try:
            if key.char is self.up:
                self.OsY = 1.0
                print("OsY = ", self.OsY)

            if key.char is self.left:
                self.OsX = -1.0
                print("OsX = ", self.OsX)

            if key.char is self.down:
                self.OsY = -1.0
                print("OsY = ", self.OsY)

            if key.char is self.right:
                self.OsX = 1.0
                print("OsX = ", self.OsX)

            if key.char is self.rotateR:
                self.rotate = 1.0
                print("rotate = ",  self.rotate)

            if key.char is self.rotateL:
                self.rotate = -1.0
                print("rotate = ", self.rotate)

            if key.char is self.goUp:
                self.OsZ = 1.0
                print("OsZ = ", self.OsZ)

            if key.char is self.goDown:
                self.OsZ = -1.0
                print("OsZ = ", self.OsZ)

            if key.char is self.close:
                print("close")
                self.listener.stop()

            print("pressed")
            self.RPI.set_engine_driver_values(self.OsY, self.OsX, self.OsZ,
                                              self.rotate, 0, 0)
            time.sleep(0.005)
        except Exception as e:
            return 0

    def on_release(self, key):
        """
        function call if any key is released
        """
        try:
            if key.char is self.up:
                self.OsY = 0.0
                print("OsY = ", self.OsY)

            if key.char is self.left:
                self.OsX = 0.0
                print("OsX = ", self.OsX)

            if key.char is self.down:
                self.OsY = 0.0
                print("OsY = ", self.OsY)

            if key.char is self.right:
                self.OsX = 0.0
                print("OsX = ", self.OsX)

            if key.char is self.rotateR:
                self.rotate = 0.0
                print("rotate = ", self.rotate)

            if key.char is self.rotateL:
                self.rotate = 0.0
                print("rotate = ", self.rotate)

            if key.char is self.goUp:
                self.OsZ = 0.0
                print("OsZ = ", self.OsZ)

            if key.char is self.goDown:
                self.OsZ = 0.0
                print("OsZ = ", self.OsZ)

            print("release")
            self.RPI.set_engine_driver_values(self.OsY, self.OsX, self.OsZ,
                                              self.rotate, 0.0, 0.0)
            time.sleep(0.005)
        except Exception as e:
            return 0

    def Start(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.listener = listener
            listener.join()

if __name__ == "__main__":
    class VirtualRpi:
        def set_engine_driver_values(self, front, right, up, yaw, pitch, roll):
            print(str(front)+" "+str(right)+" "+str(up)+" "+str(yaw)+" " +
                  str(pitch)+" "+str(roll))

    VIRTUAL_RPI = VirtualRpi()
    keyboard = KeybordControler(VIRTUAL_RPI)
    keyboard.Start()
