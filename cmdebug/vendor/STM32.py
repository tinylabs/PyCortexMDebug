#
# STM32 peripheral driver implementation
#
#
from cmdebug.periph.GPIO import GPIO
from cmdebug.periph.SPI import SPI

class STM32_GPIO (GPIO):
    def __init__(self):
        print ('STM32_GPIO loaded')

class STM32_SPI (SPI):
    def __init__(self):
        print ('STM32_SPI loaded')
