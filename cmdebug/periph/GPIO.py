#!/usr/bin/env python3
#
# Script to interact with external SPI flash
# on STM32 microcontrollers
#

import gdb
import re
import svd_hw

class GPIO:

    def __init__ (self, pin):

        # Parse pin str - ignore p before
        if pin[0] == 'p':
            pin = pin[1:]

        # Get port
        self.port = pin[0]
        if not re.match ("[a-k]", self.port):
            gdb.write ("Invalid port: {}\n".format (pin[0]))
            raise IndexError

        # Get pin
        try:
            self.pin = int (pin[1:])
        except ValueError:
            gdb.write ("Invalid pin: {}\n".format (pin[1:]))
            raise

        # Get base reg
        self.base = svd_hw().find (self.get_port())
        
        # Get GPIO fields
        self.mode = self.base.find ('moder{}'.format(self.pin))
        self.otype = self.base.find ('ot{}'.format(self.pin))
        self.pull = self.base.find ('pupdr{}'.format(self.pin))
        self.inp = self.base.find ('idr{}'.format(self.pin))
        self.out = self.base.find ('odr{}'.format(self.pin))
        
    def get_port (self):
        return 'gpio{}'.format (self.port)
    
    def config (self, cfg):
        pass

    def set (self):
        self.out.set (1)

    def clr (self):
        self.out.set (0)

    def val (self):
        return self.inp.get ()
    
    def usage (self, cmd=''):

        if cmd == 'config':
            gdb.write ('Usage: spiflash config cs=PBn spi=PBx,PBy,PBz\n')
        elif cmd == 'read':
            gdb.write ('Usage: spiflash read <addr> <len> [filename]\n')
        else:
            pass
        
    def invoke (self, args, from_tty):

        # Check usage
        if args == None:
            self.usage ()
            return
        
        # Parse args
        args = args.split (' ')
        cmd = args.pop (0).lower()
        
        

# Register command when file is sourced
if __name__ == '__main__':
    GPIO ()
