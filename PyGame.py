import pygame
import time
import os

def run(rpi_class_reference):

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Joystick Testing / XBOX360 Controller")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    joysticks = []
    clock = pygame.time.Clock()
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print("Detected joystick '",joysticks[-1].get_name(),"'")
    front = 0
    right = 0
    up = 0 
    roll = 0 
    pitch = 0
    yaw = 0
    while True:
        try:
            for event in pygame.event.get():
                #joystick_count = pygame.joystick.get_count()
                #if joystick_count == 1:
                if event.type == pygame.JOYAXISMOTION:
                    #print("Joystick '",joysticks[event.joy].get_name(),"' axis",event.axis,"motion.")
                    if event.axis == 1:
                        front = joysticks[event.joy].get_axis(event.axis)
                    elif event.axis == 4:
                        right = joysticks[event.joy].get_axis(event.axis)
                    elif event.axis == 3:
                        up = joysticks[event.joy].get_axis(event.axis)
                    elif event.axis == 2:
                        yaw = joysticks[event.joy].get_axis(event.axis)
                rpi_class_reference.movements(front,right,up,yaw,roll,pitch)
                time.sleep(0.01)
        except Exception as ex:
            print(ex)

    pygame.quit()