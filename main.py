import Pyro4
from x360pad import X360controler
import uni_pad, automat


PAD_TYPE = 'x360' # 'x360' or 'uni'


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
    elif PAD_TYPE == 'uni':
        uni_pad.run(rpi_reference)
    elif PAD_TYPE == 'auto':
        automat.run(rpi_reference)
