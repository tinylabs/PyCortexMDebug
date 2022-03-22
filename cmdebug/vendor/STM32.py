#
# Base STM32 driver. Handle all functionality common to all
# STM32 parts
#

from cmdebug.periph.Chipset import Chipset
from cmdebug.periph.GPIO import GPIO

class STM32_Chipset (Chipset):

    decoder = [
        ['base', 5], # 'STM32'
        ['family', {
            'f' : 'Foundation',
            'g' : 'Mainstream',
            'l' : 'Low_Power',
            'h' : 'High_Performance',
            'w' : 'Wireless'
        }],
        ['cpu', {
            '0' : 'CM0',
            '1' : 'CM3',
            '2' : 'CM3',
            '3' : 'CM4',
            '4' : 'CM4',
            '7' : 'CM7'
        }],
        ['family_line', 2],
        ['pin_count', {
            'f' : 20,
            'g' : 28,
            'k' : 32,
            't' : 36,
            's' : 44,
            'c' : 48,
            'r' : 64,
            'v' : 100,
            'z' : 144,
            'i' : 176
        }],
        ['flash_size', {
            '4' : 16*1024,
            '6' : 32*1024,
            '8' : 64*1024,
            'b' : 128*1024,
            'c' : 256*1024,
            'd' : 384*1024,
            'e' : 512*1024,
            'f' : 768*1024,
            'g' : 1024*1024,
            'h' : 1536*1024,
            'i' : 2048*1024
        }],
        ['package', {
            'p' : 'TSSOP',
            'h' : 'BGA',
            'u' : 'VFQFPN',
            't' : 'LQFP',
            'y' : 'WLCSP'
        }],
        ['temp', {
            '6' : '-40C to 85C',
            '7' : '-40C to 105C'
        }]
    ]

    def __init__ (self, chip_id):
        self.decoder = STM32_Chipset.decoder
        super().__init__ (chip_id)

class STM32_GPIO (GPIO):
    reg_map = {
        'mode' : ['moder{}',
                  {'input'  : 0b00,
                   'output' : 0b01,
                   'alt'    : 0b10,
                   'analog' : 0b11}],
        'type' : ['ot{}',
                  {'pushpull' : 0b0,
                   'odrain'   : 0b1}],
        'pull' : ['pupdr{}',
                  {'none' : 0b00,
                   'pullup' : 0b01,
                   'pulldown' : 0b10}],
        'inp'  : 'idr{}',
        'out'  : 'odr{}'
    }
    def __init__ (self, pin=''):
        self.port_width = 16
        self.reg_map = STM32_GPIO.reg_map
        super().__init__(pin)

