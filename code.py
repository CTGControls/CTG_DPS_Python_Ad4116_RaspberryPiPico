from CTG_AD4116Class import *
from CTG_AD4116_ import *

import board
import busio
import digitalio



ss = digitalio.DigitalInOut(board.GP9)


ss.direction = digitalio.Direction.OUTPUT
ss.value = False

_CTG_AD4116Class = CTG_AD4116Class

_CTG_AD4116_ = CTG_AD4116_

_CTG_AD4116_.startup(spiClk= 50000, CTG_AD4116= _CTG_AD4116Class)

