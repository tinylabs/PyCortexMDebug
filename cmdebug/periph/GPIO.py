#!/usr/bin/env python3
#
# Script to interact with external SPI flash
#

import gdb
import re
import cmdebug.svd_hw

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
        self.mode = self.base.find (self.reg_map['mode'].format(self.pin))
        self.ptype = self.base.find (self.reg_map['type'].format(self.pin))
        self.pull = self.base.find (self.reg_map['pull'].format(self.pin))
        self.inp = self.base.find (self.reg_map['inp'].format(self.pin))
        self.out = self.base.find (self.reg_map['out'].format(self.pin))
        
    def get_port (self):
        return 'gpio{}'.format (self.port)

    # Take config dict and call corresponding functions
    def config (self, cfg={}):
        for key in ['mode', 'pull', 'type']:
            if key in cfg.keys():
                pass

    # Set pin high
    def set (self):
        self.out.set (1)

    # Set pin low
    def clr (self):
        self.out.set (0)

    # Get value of pin
    def val (self):
        return self.inp.get ()

    # Enumerate GPIOs
    def __getitem__ (self):
        pass

    def __iter__ (self):
        pass

    def __next__ (self):
        pass

'''    
from cmdebug.utils.GDBCommand import GDBCommand
from cmdebug.vendor import VendorPeriph

class GPIOCommand (GDBCommand):
    def __init__ (self):

        # Get pins class
        gpio = VendorPeriph ('GPIO')
        
        # Get derived class
        super().__init__ ('gpio',
                          [
                              [],                    # Arbitrary name
                              [ x for x in gpio())
                          ])


'''
