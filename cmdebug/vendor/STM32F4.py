#!/usr/bin/env python3
#
# STM32 peripheral driver implementation
#
#
#import cmdebug.periph.GPIO
from cmdebug.vendor.STM32 import *

class STM32F4_GPIO (STM32_GPIO):
    def __init__(self):
        super().__init__ ()
        print ('STM32F4_GPIO loaded')
