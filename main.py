import Pyro4
from threading import Thread
from x360pad import X360controler
#from KeyboardControler import KeybordControler
#import uni_pad, automat


PAD_TYPE = 'x360pid' # 'x360' or 'x360pid' or 'uni'  or 'keyboard'


if __name__ == '__main__':
    try:
        Pyro4.locateNS()
        rpi_reference = Pyro4.Proxy("PYRONAME:RPI_communication")
    except Exception as err:
        print (err)
        exit(1)

    if PAD_TYPE == 'x360':
        pad = X360controler(rpi_reference)
        pad.Start()
    elif PAD_TYPE == 'x360pid':
        pad = X360controler(rpi_reference)
        thread = Thread(target=pad.Start)
        thread.start()
        pad.gui.run()
    elif PAD_TYPE == 'uni':
        uni_pad.run(rpi_reference)
    elif PAD_TYPE == 'auto':
        automat.run(rpi_reference)
    elif PAD_TYPE == 'keyboard':
        keyboard = KeybordControler(rpi_reference)
        keyboard.Start()
