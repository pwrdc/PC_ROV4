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
    rotateL ='l'

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


            if key.char is 'a':
                self.OsX = 1
                print("OsX = ", self.OsX)

            if key.char is 's':
                self.OsY = -1
                print("OsY = ", self.OsY)

            if key.char is 'd':
                self.OsX =-1
                print("OsX = ", self.OsX)

            if key.char is 'q':
                self.rotate = 1
                print("rotate = ",  self.rotate)

            if key.char is 'e':
                self.rotate = -1
                print("rotate = ", self.rotate)

            if key.char is 'r':
                self.OsZ = 1
                print("OsZ = ", self.OsZ)

            if key.char is 'c':
                self.OsZ = -1
                print("OsZ = ", self.OsZ)


        except:
             return 0






    def on_release(self, key):

        try:
            if key.char is 'w':
                self.OsY = 0
                print("OsY = ", self.OsY)

            if key.char is 'a':
                self.OsX = 0
                print("OsX = ", self.OsX)

            if key.char is 's':
                self.OsY = 0
                print("OsY = ", self.OsY)

            if key.char is 'd':
                self.OsX = 0
                print("OsX = ", self.OsX)

            if key.char is 'q':
                self.rotate = 0
                print("rotate = ", self.rotate)

            if key.char is 'e':
                self.rotate = 0
                print("rotate = ", self.rotate)

            if key.char is 'r':
                self.OsZ = 0
                print("OsZ = ", self.OsZ)

            if key.char is 'c':
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




