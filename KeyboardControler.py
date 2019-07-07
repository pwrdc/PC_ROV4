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

    up =     'w'
    down =   's'
    left =   'a'
    right =  'd'

    rotateR ='q'
    rotateL ='l'

    goUp =   'r'

    goDown = 'c'


    isUp = False
    isDown = False
    isLeft = False
    isRight = False
    isRotateR = False
    isRotateL = False
    isGoUP = False
    isGoDown = False

    def __init__(self, rpi_reference):
        self.RPI = rpi_reference




    def on_press(self, key):


        try:
            if key.char is self.up:
                self.isUp = True
                print("W = ", self.isUp)


            if key.char is 'a':
                self.isLeft = True
                print("A = ", self.isLeft)

            if key.char is 's':
                self.isDown = True
                print("S = ", self.isDown)

            if key.char is 'd':
                self.isRight = True
                print("D = ", self.isRight)

            if key.char is 'q':
                self.isRotateR = True
                print("Q = ",  self.isRotateR)

            if key.char is 'e':
                self.isRotateL = True
                print("R = ", self.isRotateL)

            if key.char is 'r':
                self.isGoUP = True
                print("R = ", self.isGoUP)

            if key.char is 'c':
                self.isGoDown = True
                print("C = ", self.isGoDown)
        except:
             return 0






    def on_release(self, key):

        try:
            if key.char is 'w':
                self.isUp = False
                print("W = ", self.isUp)

            if key.char is 'a':
                self.isLeft = False
                print("A = ", self.isLeft)

            if key.char is 's':
                self.isDown = False
                print("S = ", self.isDown)

            if key.char is 'd':
                self.isRight = False
                print("D = ", self.isRight)

            if key.char is 'q':
                self.isRotateR = False
                print("Q = ", self.isRotateR)

            if key.char is 'e':
                self.isRotateL = False
                print("R = ", self.isRotateL)

            if key.char is 'r':
                self.isGoUP = False
                print("R = ", self.isGoUP)

            if key.char is 'c':
                self.isGoDown = False
                print("C = ", self.isGoDown)
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





