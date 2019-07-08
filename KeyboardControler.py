import time
from threading import Thread
from pynput.keyboard import Key, Listener
import Pyro4


class KeybordControler:
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

    goDown = 'c'




    OsX = 0
    OsY = 0
    OsZ = 0
    rotate = 0

    def __init__(self, rpi_reference):
        self.RPI = rpi_reference




    def on_press(self, key):


        try:
            if key.char is self.up:
                self.OsY = 1
                print("OsY = ", self.OsY)


            if key.char is self.left:
                self.OsX = 1
                print("OsX = ", self.OsX)

            if key.char is self.down:
                self.OsY = -1
                print("OsY = ", self.OsY)

            if key.char is self.right:
                self.OsX =-1
                print("OsX = ", self.OsX)

            if key.char is self.rotateR:
                self.rotate = 1
                print("rotate = ",  self.rotate)

            if key.char is self.rotateL:
                self.rotate = -1
                print("rotate = ", self.rotate)

            if key.char is self.goUp:
                self.OsZ = 1
                print("OsZ = ", self.OsZ)

            if key.char is self.goDown:
                self.OsZ = -1
                print("OsZ = ", self.OsZ)


        except:
             return 0






    def on_release(self, key):

        try:
            if key.char is self.up:
                self.OsY = 0
                print("OsY = ", self.OsY)

            if key.char is self.left:
                self.OsX = 0
                print("OsX = ", self.OsX)

            if key.char is self.down:
                self.OsY = 0
                print("OsY = ", self.OsY)

            if key.char is self.right:
                self.OsX = 0
                print("OsX = ", self.OsX)

            if key.char is self.rotateR:
                self.rotate = 0
                print("rotate = ", self.rotate)

            if key.char is self.rotateL:
                self.rotate = 0
                print("rotate = ", self.rotate)

            if key.char is self.goUp:
                self.OsZ = 0
                print("OsZ = ", self.OsZ)

            if key.char is self.goDown:
                self.OsZ = 0
                print("OsZ = ", self.OsZ)


        except:
            return 0




    def start(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        try:
            self.RPI.set_engine_driver_values(self.engines[0] / 100, self.engines[1] / 100, self.engines[2] / 100,
                                              self.engines[3] / 100, 0, 0)
        except Exception:
            pass




